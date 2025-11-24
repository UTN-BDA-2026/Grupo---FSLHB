import csv
import os
import sys
from typing import Optional

# Permite ejecutar como 'python -m scripts.importar_arbitros [ruta_csv]'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models.arbitro import Arbitro


def importar_csv(path: str) -> tuple[int, int]:
    """Importa árbitros desde un CSV con columnas: nombre,apellido,dni.

    Devuelve (creados, omitidos_por_duplicado).
    """
    creados = 0
    omitidos = 0
    with open(path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        # Normaliza headers posibles
        field_map = {k.lower().strip(): k for k in reader.fieldnames or []}
        req = ['nombre', 'apellido', 'dni']
        if not all(h in field_map for h in req):
            raise ValueError("El CSV debe tener encabezados: nombre, apellido, dni")

        for row in reader:
            nombre = (row.get(field_map['nombre']) or '').strip()
            apellido = (row.get(field_map['apellido']) or '').strip()
            dni = (row.get(field_map['dni']) or '').strip()
            if not (nombre and apellido and dni):
                # Salta filas vacías o incompletas
                continue
            # Evita duplicados por DNI
            ya = Arbitro.query.filter_by(dni=dni).first()
            if ya:
                omitidos += 1
                continue
            db.session.add(Arbitro(nombre=nombre, apellido=apellido, dni=dni))
            creados += 1
        db.session.commit()
    return creados, omitidos


def main(csv_path: Optional[str] = None):
    # Ruta por defecto
    default_path = os.path.join('src', 'data', 'arbitros.csv')
    path = csv_path or default_path
    if not os.path.exists(path):
        print(f"No se encontró el archivo CSV en: {path}")
        print("Crea el archivo con encabezados 'nombre,apellido,dni' o pasa la ruta como argumento.")
        return

    with app.app_context():
        creados, omitidos = importar_csv(path)
        print(f"Árbitros importados: {creados}. Duplicados omitidos (por DNI): {omitidos}.")


if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)
