import sys
from pathlib import Path
# Asegura que el directorio raíz (que contiene el paquete 'app') esté en sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
root_str = str(ROOT_DIR)
if root_str not in sys.path:
    sys.path.insert(0, root_str)
from app import app
from app.services.partido_fixture_service import cargar_partidos_desde_csv_fileobj

"""
Uso: ejecutar dentro del contexto Flask para cargar partidos desde un CSV.
Formato CSV (cabeceras): torneo,categoria,fecha_numero,bloque,fecha_hora,cancha,equipo_local_nombre,equipo_visitante_nombre
- fecha_hora: ISO (ej. 2025-10-11T16:30) o vacía
- Los equipos se ubican por nombre exacto; si hay múltiples, refine con categoría.

Ejemplo:
Clausura Damas (2025),damas_b,12,C,2025-10-11T16:30,SR Tenis,LOS TORDOS,SR TENIS
"""


def cargar_desde_csv(path: str):
    with app.app_context():
        with open(path, newline='', encoding='utf-8') as f:
            count = cargar_partidos_desde_csv_fileobj(f)
            print(f'Creados {count} partidos')

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Uso: python -m scripts.admin_cargar_partidos <archivo.csv>')
        sys.exit(1)
    cargar_desde_csv(sys.argv[1])
