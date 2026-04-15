import csv
from datetime import datetime

from app import db
from app.models.partido import Partido
from app.models.club import Club
from app.models.equipo import Equipo


def _buscar_club(nombre: str):
    return db.session.query(Club).filter(Club.nombre == nombre).first()


def _buscar_equipo(nombre: str, categoria: str | None = None):
    q = db.session.query(Equipo).filter(Equipo.nombre == nombre)
    if categoria:
        q = q.filter(Equipo.categoria == categoria)
    return q.first()


def cargar_partidos_desde_csv_reader(reader) -> int:
    """Carga partidos a partir de un csv.DictReader.

    No maneja app_context; el llamador debe estar dentro del contexto Flask.
    Devuelve la cantidad de partidos creados.
    """
    from app.repositories.torneo_repositorio import TorneoRepository
    from app.repositories.partido_repositorio import PartidoRepository

    count = 0
    torneos = TorneoRepository.obtener_torneos()
    fechas_por_torneo: dict[str, set[int]] = {}

    for row in reader:
        torneo = row.get('torneo')
        categoria = row.get('categoria')
        fecha_numero = row.get('fecha_numero')
        bloque = row.get('bloque')
        fecha_hora = row.get('fecha_hora')
        cancha = row.get('cancha')
        local_nombre = row.get('equipo_local_nombre')
        visit_nombre = row.get('equipo_visitante_nombre')

        if not torneo or not categoria or not local_nombre or not visit_nombre:
            # Fila incompleta, se omite
            continue

        torneo_info = next((t for t in torneos if t['nombre'] == torneo), None)
        if torneo_info:
            max_fechas = torneo_info['max_fechas']
            if torneo not in fechas_por_torneo:
                fechas_db = set(
                    p.fecha_numero for p in PartidoRepository.buscar({'torneo': torneo}) if p.fecha_numero is not None
                )
                fechas_por_torneo[torneo] = fechas_db
            fechas_actual = fechas_por_torneo[torneo]
            fecha_num = int(fecha_numero) if fecha_numero else None
            if fecha_num is not None and fecha_num not in fechas_actual and len(fechas_actual) >= max_fechas:
                # Límite de fechas alcanzado para este torneo
                continue
            if fecha_num is not None:
                fechas_actual.add(fecha_num)

        eq_local = _buscar_equipo(local_nombre, categoria)
        eq_visit = _buscar_equipo(visit_nombre, categoria)
        cl_local = eq_local.club if eq_local else _buscar_club(local_nombre)
        cl_visit = eq_visit.club if eq_visit else _buscar_club(visit_nombre)
        if not cl_local or not cl_visit:
            # No se encontró club local o visitante, se omite
            continue

        fh = None
        if fecha_hora:
            try:
                fh = datetime.fromisoformat(fecha_hora)
            except Exception:
                fh = None

        p = Partido(
            torneo=torneo,
            categoria=categoria,
            fecha_numero=int(fecha_numero) if fecha_numero else None,
            bloque=bloque or None,
            fecha_hora=fh,
            cancha=cancha or None,
            club_local_id=cl_local.id,
            club_visitante_id=cl_visit.id,
            equipo_local_id=eq_local.id if eq_local else None,
            equipo_visitante_id=eq_visit.id if eq_visit else None,
        )
        db.session.add(p)
        count += 1

    db.session.commit()
    return count


def cargar_partidos_desde_csv_fileobj(file_obj) -> int:
    """Carga partidos leyendo un archivo CSV (file-like en texto)."""
    reader = csv.DictReader(file_obj)
    return cargar_partidos_desde_csv_reader(reader)
