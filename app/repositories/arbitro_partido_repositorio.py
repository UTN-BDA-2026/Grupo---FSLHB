from app import db
from app.models.arbitro_partido import ArbitroPartido
from app.models.arbitro import Arbitro
from sqlalchemy.exc import OperationalError, ProgrammingError

# Nota: algunos entornos aún no aplicaron la migración que agrega 'club_id'.
# Este repositorio intenta primero usar 'club_id'; si la columna no existe,
# hace fallback a usar el campo 'rol' con valores 'local'/'visit'.


class ArbitroPartidoRepositorio:
    @staticmethod
    def listar_por_partido(partido_id: int):
        try:
            return (
                db.session.query(ArbitroPartido, Arbitro)
                .join(Arbitro, ArbitroPartido.arbitro_id == Arbitro.id)
                .filter(ArbitroPartido.partido_id == partido_id)
                .order_by(Arbitro.apellido, Arbitro.nombre)
                .all()
            )
        except (OperationalError, ProgrammingError):
            # Fallback para esquemas sin columna club_id: usar consulta textual
            db.session.rollback()
            from types import SimpleNamespace
            from sqlalchemy import text
            sql = text(
                """
                SELECT ap.id AS ap_id, ap.partido_id AS ap_partido_id, ap.arbitro_id AS ap_arbitro_id, ap.rol AS ap_rol,
                       a.id AS a_id, a.nombre AS a_nombre, a.apellido AS a_apellido, a.dni AS a_dni
                FROM arbitro_partido ap
                JOIN arbitros a ON ap.arbitro_id = a.id
                WHERE ap.partido_id = :pid
                ORDER BY a.apellido, a.nombre
                """
            )
            rows = db.session.execute(sql, {"pid": partido_id}).fetchall()
            result = []
            for r in rows:
                ap_ns = SimpleNamespace(id=r.ap_id, partido_id=r.ap_partido_id, arbitro_id=r.ap_arbitro_id, rol=r.ap_rol)
                a_ns = SimpleNamespace(id=r.a_id, nombre=r.a_nombre, apellido=r.a_apellido, dni=r.a_dni)
                result.append((ap_ns, a_ns))
            return result

    @staticmethod
    def set_por_equipo(partido_id: int, club_id: int, arbitro_id: int | None):
        try:
            existente = ArbitroPartido.query.filter_by(partido_id=partido_id, club_id=club_id).first()
            if arbitro_id is None:
                if existente:
                    db.session.delete(existente)
                    db.session.commit()
                return None
            # Upsert por (partido_id, club_id)
            if existente:
                existente.arbitro_id = int(arbitro_id)
            else:
                db.session.add(ArbitroPartido(partido_id=partido_id, club_id=club_id, arbitro_id=int(arbitro_id)))
            db.session.commit()
            return ArbitroPartido.query.filter_by(partido_id=partido_id, club_id=club_id).first()
        except (OperationalError, ProgrammingError):
            # Fallback: base sin columna club_id -> usar SQL crudo sobre 'rol'
            db.session.rollback()
            from sqlalchemy import text
            from types import SimpleNamespace
            # Resolver side comparando con el partido
            from app.services.partido_service import PartidoService
            p = PartidoService.obtener_por_id(partido_id)
            side = None
            if getattr(p, 'club_local_id', None) == club_id:
                side = 'local'
            elif getattr(p, 'club_visitante_id', None) == club_id:
                side = 'visit'
            if not side:
                side = f'club_{club_id}'

            # Buscar existente sin tocar el ORM (evitar columnas inexistentes)
            row = db.session.execute(
                text('SELECT id FROM arbitro_partido WHERE partido_id=:pid AND rol=:rol LIMIT 1'),
                {"pid": partido_id, "rol": side}
            ).fetchone()

            if arbitro_id is None:
                if row:
                    db.session.execute(text('DELETE FROM arbitro_partido WHERE id=:id'), {"id": row.id})
                    db.session.commit()
                return None

            if row:
                db.session.execute(
                    text('UPDATE arbitro_partido SET arbitro_id=:aid WHERE id=:id'),
                    {"aid": int(arbitro_id), "id": row.id}
                )
            else:
                db.session.execute(
                    text('INSERT INTO arbitro_partido (partido_id, arbitro_id, rol) VALUES (:pid, :aid, :rol)'),
                    {"pid": partido_id, "aid": int(arbitro_id), "rol": side}
                )
            db.session.commit()

            # Devolver un objeto compatible mínimo
            new_row = db.session.execute(
                text('SELECT id, partido_id, arbitro_id, rol FROM arbitro_partido WHERE partido_id=:pid AND rol=:rol ORDER BY id DESC LIMIT 1'),
                {"pid": partido_id, "rol": side}
            ).fetchone()
            return SimpleNamespace(id=new_row.id, partido_id=new_row.partido_id, arbitro_id=new_row.arbitro_id, rol=new_row.rol)
