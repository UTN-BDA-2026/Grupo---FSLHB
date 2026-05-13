"""Migración Postgres -> MongoDB para este proyecto.

Contexto
- El repo actualmente usa MongoDB (Flask-PyMongo) para la app.
- En algunos entornos existe un dump de Postgres (pg_dump custom, .dump).
- Este script lee tablas de Postgres y las inserta en las colecciones Mongo
  con el formato esperado por los modelos/repositories del proyecto.

Cómo usar (por defecto asume contenedores Docker expuestos en localhost):

  # 1) Asegurate de tener Postgres con datos (ej: restaurado desde backup_local.dump)
  # 2) Migrar a Mongo (sin borrar nada):
  python scripts/migrate_postgres_to_mongodb.py

  # Migrar borrando primero las colecciones destino:
  python scripts/migrate_postgres_to_mongodb.py --wipe-mongo

Parámetros (opcionales):
- Postgres: --pg-host --pg-port --pg-db --pg-user --pg-password
- Mongo: --mongo-uri (si no, toma MONGO_URI o usa localhost)

Notas
- Se guarda el id original de Postgres en `legacy_pg` para trazabilidad.
- Se crean ObjectId nuevos y se resuelven relaciones vía mapas legacy_id -> ObjectId.
"""

from __future__ import annotations

import argparse
import os
from datetime import date, datetime, time
from decimal import Decimal
from typing import Any, Callable, Iterable

import psycopg
from psycopg.rows import dict_row
from pymongo import MongoClient
from bson import ObjectId


def _norm_key(key: str) -> str:
    return ''.join(ch for ch in key.lower() if ch.isalnum())


def _row_index(row: dict[str, Any]) -> dict[str, str]:
    """Map normalized_key -> original_key."""
    idx: dict[str, str] = {}
    for k in row.keys():
        nk = _norm_key(k)
        if nk not in idx:
            idx[nk] = k
    return idx


def _get(row: dict[str, Any], *candidates: str, default: Any = None) -> Any:
    if not row:
        return default
    idx = _row_index(row)
    for cand in candidates:
        k = idx.get(_norm_key(cand))
        if k is None:
            continue
        v = row.get(k)
        if v is not None:
            return v
    return default


def _as_bool(v: Any, default: bool = False) -> bool:
    if v is None:
        return default
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return bool(v)
    if isinstance(v, str):
        s = v.strip().lower()
        if s in ('1', 'true', 't', 'yes', 'y', 'si', 'sí'):
            return True
        if s in ('0', 'false', 'f', 'no', 'n'):
            return False
    return default


def _to_bson(v: Any) -> Any:
    if v is None:
        return None
    if isinstance(v, datetime):
        return v
    if isinstance(v, date) and not isinstance(v, datetime):
        # BSON no soporta date puro
        return datetime(v.year, v.month, v.day)
    if isinstance(v, time):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    # UUID, enums, etc.
    if hasattr(v, 'hex') and not isinstance(v, (bytes, bytearray)):
        try:
            return str(v)
        except Exception:
            pass
    return v


def _legacy_id(row: dict[str, Any]) -> Any:
    return _get(row, 'id', 'ID', 'Id', default=None)


def _connect_pg(args) -> psycopg.Connection:
    dsn = args.pg_dsn
    if not dsn:
        dsn = (
            f"postgresql://{args.pg_user}:{args.pg_password}"
            f"@{args.pg_host}:{args.pg_port}/{args.pg_db}"
        )
    return psycopg.connect(dsn, row_factory=dict_row)


def _connect_mongo(args) -> tuple[MongoClient, Any]:
    mongo_uri = args.mongo_uri or os.getenv('MONGO_URI')
    if not mongo_uri:
        mongo_uri = 'mongodb://admin:adminpass@localhost:27017/hockey?authSource=admin'
    client = MongoClient(mongo_uri)
    db = client.get_default_database()
    if db is None:
        db = client['hockey']
    # Ping
    db.command('ping')
    return client, db


def _pg_tables(conn: psycopg.Connection) -> set[str]:
    rows = conn.execute(
        """
        select table_name
        from information_schema.tables
        where table_schema = 'public' and table_type='BASE TABLE'
        """
    ).fetchall()
    return {r['table_name'] for r in rows}


def _fetch_all(conn: psycopg.Connection, table_name: str) -> list[dict[str, Any]]:
    from psycopg import sql

    q = sql.SQL('select * from {}').format(sql.Identifier(table_name))
    return list(conn.execute(q).fetchall())


def _wipe(db, collections: Iterable[str]) -> None:
    for c in collections:
        db[c].delete_many({})


def _insert_if_missing(col, doc: dict[str, Any], legacy_table: str, legacy_id_value: Any, *, dry_run: bool) -> ObjectId:
    """Insert a document if no doc with legacy_pg matches; returns _id."""
    if legacy_id_value is not None:
        existing = col.find_one({'legacy_pg.table': legacy_table, 'legacy_pg.id': legacy_id_value}, {'_id': 1})
        if existing:
            return existing['_id']

    oid = doc.get('_id') or ObjectId()
    doc['_id'] = oid

    # Convert values for BSON
    for k, v in list(doc.items()):
        doc[k] = _to_bson(v)

    if legacy_id_value is not None:
        doc['legacy_pg'] = {'table': legacy_table, 'id': legacy_id_value}

    if not dry_run:
        col.insert_one(doc)
    return oid


def migrate_clubes(pg: psycopg.Connection, db, *, dry_run: bool) -> dict[Any, ObjectId]:
    table = 'Clubes'
    if table not in _pg_tables(pg):
        return {}

    rows = _fetch_all(pg, table)
    col = db['clubes']
    id_map: dict[Any, ObjectId] = {}

    for r in rows:
        lid = _legacy_id(r)
        doc = {
            'nombre': _get(r, 'nombre', 'name', default=''),
            'razon_social': _get(r, 'razon_social', 'razonsocial', 'razon', default=None),
            'contacto': _get(r, 'contacto', default=None),
            'email': _get(r, 'email', 'mail', default=None),
            'cancha_local': _get(r, 'cancha_local', 'cancha', default=None),
            'domicilio': _get(r, 'domicilio', 'direccion', default=None),
            'telefono': _get(r, 'telefono', 'tel', default=None),
            'web': _get(r, 'web', 'sitio', default=None),
            # arbitro_id se setea luego si se migra arbitros
            'arbitro_id': None,
        }
        oid = _insert_if_missing(col, doc, table, lid, dry_run=dry_run)
        if lid is not None:
            id_map[lid] = oid
    return id_map


def migrate_equipos(pg: psycopg.Connection, db, club_map: dict[Any, ObjectId], *, dry_run: bool) -> dict[Any, ObjectId]:
    table = 'Equipos'
    if table not in _pg_tables(pg):
        return {}

    rows = _fetch_all(pg, table)
    col = db['equipos']
    id_map: dict[Any, ObjectId] = {}

    for r in rows:
        lid = _legacy_id(r)
        club_fk = _get(r, 'club_id', 'id_club', 'club', 'clubid', default=None)
        club_oid = club_map.get(club_fk)

        doc = {
            'nombre': _get(r, 'nombre', 'name', default=''),
            'categoria': _get(r, 'categoria', 'category', default=None),
            'club_id': club_oid,
        }

        oid = _insert_if_missing(col, doc, table, lid, dry_run=dry_run)
        if lid is not None:
            id_map[lid] = oid
    return id_map


def migrate_jugadoras(pg: psycopg.Connection, db, club_map: dict[Any, ObjectId], *, dry_run: bool) -> dict[Any, ObjectId]:
    table = 'Jugadoras'
    if table not in _pg_tables(pg):
        return {}

    rows = _fetch_all(pg, table)
    col = db['jugadoras']
    id_map: dict[Any, ObjectId] = {}

    for r in rows:
        lid = _legacy_id(r)
        club_fk = _get(r, 'club_id', 'id_club', 'club', 'clubid', default=None)
        club_oid = club_map.get(club_fk)

        doc = {
            'nombre': _get(r, 'nombre', 'name', default=''),
            'apellido': _get(r, 'apellido', 'last_name', 'lastname', default=''),
            'dni': _get(r, 'dni', default=None),
            'fecha_nacimiento': _get(r, 'fecha_nacimiento', 'fechanacimiento', 'nacimiento', default=None),
            'categoria': _get(r, 'categoria', default=None),
            'club_id': club_oid,
        }

        oid = _insert_if_missing(col, doc, table, lid, dry_run=dry_run)
        if lid is not None:
            id_map[lid] = oid
    return id_map


def migrate_torneos(pg: psycopg.Connection, db, *, dry_run: bool) -> dict[Any, ObjectId]:
    table = 'torneos'
    if table not in _pg_tables(pg):
        # algunas bases lo guardan como Torneos (capitalizado)
        if 'Torneos' in _pg_tables(pg):
            table = 'Torneos'
        else:
            return {}

    rows = _fetch_all(pg, table)
    col = db['torneos']
    id_map: dict[Any, ObjectId] = {}

    for r in rows:
        lid = _legacy_id(r)
        doc = {
            'nombre': _get(r, 'nombre', 'name', default=''),
            'max_fechas': _get(r, 'max_fechas', 'maxfechas', 'max_fechas_por_torneo', default=0),
        }
        oid = _insert_if_missing(col, doc, table, lid, dry_run=dry_run)
        if lid is not None:
            id_map[lid] = oid
    return id_map


def _torneo_nombre_from_fk(row: dict[str, Any], torneos_rows_by_id: dict[Any, dict[str, Any]]) -> str | None:
    torneo_name = _get(row, 'torneo', 'torneo_nombre', 'torneonombre', default=None)
    if torneo_name:
        return str(torneo_name)

    torneo_fk = _get(row, 'torneo_id', 'id_torneo', 'torneoid', default=None)
    if torneo_fk is not None and torneo_fk in torneos_rows_by_id:
        return str(_get(torneos_rows_by_id[torneo_fk], 'nombre', 'name', default=torneo_fk))

    if torneo_fk is not None:
        return str(torneo_fk)

    return None


def migrate_partidos(
    pg: psycopg.Connection,
    db,
    club_map: dict[Any, ObjectId],
    equipo_map: dict[Any, ObjectId],
    torneos_rows_by_id: dict[Any, dict[str, Any]],
    *,
    dry_run: bool,
) -> dict[Any, ObjectId]:
    table = 'Partidos'
    if table not in _pg_tables(pg):
        return {}

    rows = _fetch_all(pg, table)
    col = db['partidos']
    id_map: dict[Any, ObjectId] = {}

    for r in rows:
        lid = _legacy_id(r)

        torneo_nombre = _torneo_nombre_from_fk(r, torneos_rows_by_id)

        club_local_fk = _get(r, 'club_local_id', 'id_club_local', 'club_local', 'clublocalid', default=None)
        club_visit_fk = _get(r, 'club_visitante_id', 'id_club_visitante', 'club_visitante', 'clubvisitanteid', default=None)
        club_local_oid = club_map.get(club_local_fk)
        club_visit_oid = club_map.get(club_visit_fk)

        equipo_local_fk = _get(r, 'equipo_local_id', 'id_equipo_local', 'equipo_local', 'equipolocalid', default=None)
        equipo_visit_fk = _get(r, 'equipo_visitante_id', 'id_equipo_visitante', 'equipo_visitante', 'equipovisitanteid', default=None)
        equipo_local_oid = equipo_map.get(equipo_local_fk)
        equipo_visit_oid = equipo_map.get(equipo_visit_fk)

        fecha_hora = _get(r, 'fecha_hora', 'fecha', 'datetime', 'fechaHora', default=None)

        doc = {
            'torneo': torneo_nombre,
            'categoria': _get(r, 'categoria', default=None),
            'fecha_numero': _get(r, 'fecha_numero', 'fecha', 'fechanumero', default=None),
            'bloque': _get(r, 'bloque', default=None),
            'fecha_hora': fecha_hora,
            'cancha': _get(r, 'cancha', default=None),
            'club_local_id': club_local_oid,
            'club_visitante_id': club_visit_oid,
            'equipo_local_id': equipo_local_oid,
            'equipo_visitante_id': equipo_visit_oid,
            'estado': _get(r, 'estado', default='programado') or 'programado',
            'goles_local': _get(r, 'goles_local', 'goleslocal', default=None),
            'goles_visitante': _get(r, 'goles_visitante', 'golesvisitante', default=None),
        }

        oid = _insert_if_missing(col, doc, table, lid, dry_run=dry_run)
        if lid is not None:
            id_map[lid] = oid

    return id_map


def migrate_resultados(
    pg: psycopg.Connection,
    db,
    club_map: dict[Any, ObjectId],
    partido_map: dict[Any, ObjectId],
    *,
    dry_run: bool,
) -> int:
    table = 'Resultados'
    if table not in _pg_tables(pg):
        return 0

    rows = _fetch_all(pg, table)
    col = db['resultados']
    inserted = 0

    for r in rows:
        lid = _legacy_id(r)
        partido_fk = _get(r, 'partido_id', 'id_partido', 'partido', default=None)
        club_local_fk = _get(r, 'club_local_id', 'id_club_local', 'club_local', default=None)
        club_visit_fk = _get(r, 'club_visitante_id', 'id_club_visitante', 'club_visitante', default=None)

        doc = {
            'club_local': str(club_map.get(club_local_fk) or club_local_fk) if (club_local_fk is not None) else None,
            'club_visitante': str(club_map.get(club_visit_fk) or club_visit_fk) if (club_visit_fk is not None) else None,
            'goles_local': _get(r, 'goles_local', 'goleslocal', default=None),
            'goles_visitante': _get(r, 'goles_visitante', 'golesvisitante', default=None),
            'fecha': _get(r, 'fecha', 'fecha_hora', default=None),
        }

        _insert_if_missing(col, doc, table, lid, dry_run=dry_run)
        inserted += 1

        # Si podemos, actualizamos el partido en Mongo con el resultado
        partido_oid = partido_map.get(partido_fk)
        if partido_oid and not dry_run:
            upd = {
                'goles_local': doc['goles_local'],
                'goles_visitante': doc['goles_visitante'],
                'estado': 'jugado',
            }
            db['partidos'].update_one({'_id': partido_oid}, {'$set': upd})

    return inserted


def migrate_incidencias(
    pg: psycopg.Connection,
    db,
    club_map: dict[Any, ObjectId],
    jugadora_map: dict[Any, ObjectId],
    partido_map: dict[Any, ObjectId],
    *,
    dry_run: bool,
) -> int:
    table = 'Incidencias'
    if table not in _pg_tables(pg):
        return 0

    rows = _fetch_all(pg, table)
    col = db['incidencias']
    inserted = 0

    for r in rows:
        lid = _legacy_id(r)
        partido_fk = _get(r, 'partido_id', 'id_partido', 'partido', default=None)
        club_fk = _get(r, 'club_id', 'id_club', 'club', default=None)
        jugadora_fk = _get(r, 'jugadora_id', 'id_jugadora', 'jugadora', default=None)

        raw_tipo = _get(r, 'tipo', 'tipo_incidencia', 'tipoincidencia', default=None)
        tipo = None
        color = None
        if raw_tipo is not None:
            s = str(raw_tipo).lower()
            if 'gol' in s:
                tipo = 'gol'
            elif 'tarjeta' in s or 'verde' in s or 'amarilla' in s or 'roja' in s:
                tipo = 'tarjeta'
                if 'verde' in s:
                    color = 'verde'
                elif 'amarilla' in s:
                    color = 'amarilla'
                elif 'roja' in s:
                    color = 'roja'
            else:
                tipo = str(raw_tipo)

        doc = {
            'partido_id': partido_map.get(partido_fk),
            'club_id': club_map.get(club_fk),
            'jugadora_id': jugadora_map.get(jugadora_fk),
            'tipo': tipo,
            'color': color or _get(r, 'color', default=None),
            'minuto': _get(r, 'minuto', default=None),
            'created_at': _get(r, 'created_at', 'fecha', default=None) or datetime.utcnow(),
        }

        _insert_if_missing(col, doc, table, lid, dry_run=dry_run)
        inserted += 1

    return inserted


def migrate_noticias(pg: psycopg.Connection, db, *, dry_run: bool) -> int:
    table = 'noticia'
    if table not in _pg_tables(pg):
        if 'Noticias' in _pg_tables(pg):
            table = 'Noticias'
        else:
            return 0

    rows = _fetch_all(pg, table)
    col = db['noticias']
    inserted = 0

    for r in rows:
        lid = _legacy_id(r)
        doc = {
            'titulo': _get(r, 'titulo', 'title', default=''),
            'resumen': _get(r, 'resumen', 'summary', default=None),
            'contenido': _get(r, 'contenido', 'content', default=''),
            'imagen': _get(r, 'imagen', 'image', default=None),
            'fecha': _get(r, 'fecha', 'created_at', default=None),
        }
        _insert_if_missing(col, doc, table, lid, dry_run=dry_run)
        inserted += 1

    return inserted


def migrate_notas_partido(
    pg: psycopg.Connection,
    db,
    partido_map: dict[Any, ObjectId],
    *,
    dry_run: bool,
) -> int:
    table = 'NotasPartido'
    if table not in _pg_tables(pg):
        return 0

    rows = _fetch_all(pg, table)
    col = db['notas_partido']
    inserted = 0

    for r in rows:
        lid = _legacy_id(r)
        partido_fk = _get(r, 'partido_id', 'id_partido', 'partido', default=None)
        doc = {
            'partido_id': partido_map.get(partido_fk),
            'detalle': _get(r, 'detalle', 'nota', 'descripcion', default=None),
        }
        _insert_if_missing(col, doc, table, lid, dry_run=dry_run)
        inserted += 1

    return inserted


def migrate_usuarios(pg: psycopg.Connection, db, club_map: dict[Any, ObjectId], *, dry_run: bool) -> int:
    table = 'usuarios'
    if table not in _pg_tables(pg):
        return 0

    rows = _fetch_all(pg, table)
    col = db['usuarios']
    inserted = 0

    for r in rows:
        lid = _legacy_id(r)
        club_fk = _get(r, 'club_id', 'id_club', 'club', default=None)
        doc = {
            'username': _get(r, 'username', 'usuario', 'user', default=''),
            'password': _get(r, 'password', 'contrasena', 'contraseña', default=''),
            'club_id': club_map.get(club_fk),
            'is_operador': _as_bool(_get(r, 'is_operador', 'operador', default=False)),
            'puede_cargar_incidencias': _as_bool(_get(r, 'puede_cargar_incidencias', 'puedeCargarIncidencias', default=False)),
            'puede_precargar_equipos': _as_bool(_get(r, 'puede_precargar_equipos', 'puedePrecargarEquipos', default=False)),
            'is_admin': _as_bool(_get(r, 'is_admin', 'admin', default=False)),
        }
        _insert_if_missing(col, doc, table, lid, dry_run=dry_run)
        inserted += 1

    return inserted


def main() -> int:
    parser = argparse.ArgumentParser(description='Migra datos de Postgres (docker) a MongoDB (app).')

    parser.add_argument('--pg-dsn', default=os.getenv('SOURCE_DATABASE_URL') or os.getenv('DATABASE_URL'))
    parser.add_argument('--pg-host', default=os.getenv('PGHOST', 'localhost'))
    parser.add_argument('--pg-port', default=int(os.getenv('PGPORT', '5433')))
    parser.add_argument('--pg-db', default=os.getenv('PGDATABASE', 'hockey'))
    parser.add_argument('--pg-user', default=os.getenv('PGUSER', 'hockeyuser'))
    parser.add_argument('--pg-password', default=os.getenv('PGPASSWORD', 'hockeypass'))

    parser.add_argument('--mongo-uri', default=None)

    parser.add_argument('--wipe-mongo', action='store_true', help='Borra colecciones destino antes de migrar')
    parser.add_argument('--dry-run', action='store_true', help='No escribe en MongoDB (solo conecta y recorre)')

    args = parser.parse_args()

    mongo_client = None
    pg_conn = None

    try:
        pg_conn = _connect_pg(args)
        mongo_client, mongo_db = _connect_mongo(args)

        tables = _pg_tables(pg_conn)
        print(f"✓ Postgres conectado. Tablas public: {len(tables)}")
        print(f"✓ MongoDB conectado. DB: {mongo_db.name}")

        target_cols = [
            'clubes', 'equipos', 'jugadoras', 'torneos', 'partidos',
            'resultados', 'incidencias', 'noticias', 'notas_partido', 'usuarios'
        ]

        if args.wipe_mongo:
            print('⚠️  wipe-mongo: borrando colecciones destino...')
            if not args.dry_run:
                _wipe(mongo_db, target_cols)

        # Torneos (para resolver nombre desde fk)
        torneos_table = 'torneos' if 'torneos' in tables else ('Torneos' if 'Torneos' in tables else None)
        torneos_rows_by_id: dict[Any, dict[str, Any]] = {}
        if torneos_table:
            for tr in _fetch_all(pg_conn, torneos_table):
                lid = _legacy_id(tr)
                if lid is not None:
                    torneos_rows_by_id[lid] = tr

        club_map = migrate_clubes(pg_conn, mongo_db, dry_run=args.dry_run)
        print(f"✓ Clubes migrados: {len(club_map)}")

        equipo_map = migrate_equipos(pg_conn, mongo_db, club_map, dry_run=args.dry_run)
        print(f"✓ Equipos migrados: {len(equipo_map)}")

        jugadora_map = migrate_jugadoras(pg_conn, mongo_db, club_map, dry_run=args.dry_run)
        print(f"✓ Jugadoras migradas: {len(jugadora_map)}")

        torneo_map = migrate_torneos(pg_conn, mongo_db, dry_run=args.dry_run)
        print(f"✓ Torneos migrados: {len(torneo_map)}")

        partido_map = migrate_partidos(
            pg_conn,
            mongo_db,
            club_map,
            equipo_map,
            torneos_rows_by_id,
            dry_run=args.dry_run,
        )
        print(f"✓ Partidos migrados: {len(partido_map)}")

        resultados_n = migrate_resultados(pg_conn, mongo_db, club_map, partido_map, dry_run=args.dry_run)
        print(f"✓ Resultados migrados: {resultados_n}")

        incidencias_n = migrate_incidencias(pg_conn, mongo_db, club_map, jugadora_map, partido_map, dry_run=args.dry_run)
        print(f"✓ Incidencias migradas: {incidencias_n}")

        noticias_n = migrate_noticias(pg_conn, mongo_db, dry_run=args.dry_run)
        print(f"✓ Noticias migradas: {noticias_n}")

        notas_n = migrate_notas_partido(pg_conn, mongo_db, partido_map, dry_run=args.dry_run)
        print(f"✓ Notas de partido migradas: {notas_n}")

        usuarios_n = migrate_usuarios(pg_conn, mongo_db, club_map, dry_run=args.dry_run)
        print(f"✓ Usuarios migrados: {usuarios_n}")

        print('✅ Migración completa')
        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    finally:
        try:
            if pg_conn is not None:
                pg_conn.close()
        except Exception:
            pass
        try:
            if mongo_client is not None:
                mongo_client.close()
        except Exception:
            pass


if __name__ == '__main__':
    raise SystemExit(main())
