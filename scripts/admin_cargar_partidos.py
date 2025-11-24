import csv
from datetime import datetime
from app import app, db
from app.models.partido import Partido
from app.models.club import Club
from app.models.equipo import Equipo

"""
Uso: ejecutar dentro del contexto Flask para cargar partidos desde un CSV.
Formato CSV (cabeceras): torneo,categoria,fecha_numero,bloque,fecha_hora,cancha,equipo_local_nombre,equipo_visitante_nombre
- fecha_hora: ISO (ej. 2025-10-11T16:30) o vacía
- Los equipos se ubican por nombre exacto; si hay múltiples, refine con categoría.

Ejemplo:
Clausura Damas (2025),damas_b,12,C,2025-10-11T16:30,SR Tenis,LOS TORDOS,SR TENIS
"""

def buscar_club(nombre: str):
    return db.session.query(Club).filter(Club.nombre == nombre).first()

def buscar_equipo(nombre: str, categoria: str = None):
    q = db.session.query(Equipo).filter(Equipo.nombre == nombre)
    if categoria:
        q = q.filter(Equipo.categoria == categoria)
    return q.first()


def cargar_desde_csv(path: str):
    with app.app_context():
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            # --- Validación de límite de fechas por torneo ---
            from app.repositories.torneo_repositorio import TorneoRepository
            from app.repositories.partido_repositorio import PartidoRepository
            torneos = TorneoRepository.obtener_torneos()
            fechas_por_torneo = {}
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
                    print('Fila incompleta, se omite:', row)
                    continue

                torneo_info = next((t for t in torneos if t['nombre'] == torneo), None)
                if torneo_info:
                    max_fechas = torneo_info['max_fechas']
                    # Obtener fechas ya jugadas en la base de datos y en el lote actual
                    if torneo not in fechas_por_torneo:
                        fechas_db = set(
                            p.fecha_numero for p in PartidoRepository.buscar({'torneo': torneo}) if p.fecha_numero is not None
                        )
                        fechas_por_torneo[torneo] = fechas_db
                    fechas_actual = fechas_por_torneo[torneo]
                    fecha_num = int(fecha_numero) if fecha_numero else None
                    if fecha_num is not None and fecha_num not in fechas_actual and len(fechas_actual) >= max_fechas:
                        print(f'No se puede agregar la fecha {fecha_num} al torneo {torneo}: límite de {max_fechas} fechas alcanzado.')
                        continue
                    if fecha_num is not None:
                        fechas_actual.add(fecha_num)

                # Intentar resolver por equipo primero (para diferenciar A/B)
                eq_local = buscar_equipo(local_nombre, categoria)
                eq_visit = buscar_equipo(visit_nombre, categoria)
                cl_local = eq_local.club if eq_local else buscar_club(local_nombre)
                cl_visit = eq_visit.club if eq_visit else buscar_club(visit_nombre)
                if not cl_local or not cl_visit:
                    print('No se encontró club local o visitante para fila:', row)
                    continue

                fh = None
                if fecha_hora:
                    try:
                        fh = datetime.fromisoformat(fecha_hora)
                    except Exception:
                        print('fecha_hora inválida, se deja en None:', fecha_hora)

                # Usar club_id en vez de equipo_id
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
            print(f'Creados {count} partidos')

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Uso: python -m scripts.admin_cargar_partidos <archivo.csv>')
        sys.exit(1)
    cargar_desde_csv(sys.argv[1])
