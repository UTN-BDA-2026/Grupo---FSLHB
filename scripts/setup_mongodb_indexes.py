"""
Inicializa índices de MongoDB para optimizar búsquedas.

Este script debe ejecutarse una sola vez después de crear la base de datos.
Uso: python scripts/setup_mongodb_indexes.py
"""

import sys
from pathlib import Path

# Agregar app al path
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from app import app
from app.extensions import mongo


def setup_indexes():
    """Crea índices en las colecciones de MongoDB."""
    with app.app_context():
        db = mongo.db
        
        # Índices en usuarios
        db.usuarios.create_index([('username', 1)], unique=True)
        print("✓ Índice único en usuarios.username")
        
        # Índices en clubes
        db.clubes.create_index([('nombre', 1)], unique=True)
        print("✓ Índice único en clubes.nombre")
        
        # Índices en equipos
        db.equipos.create_index([('nombre', 1)], unique=True)
        print("✓ Índice único en equipos.nombre")
        
        # Índices en partidos (búsquedas frecuentes)
        db.partidos.create_index([('fecha', -1)])
        print("✓ Índice en partidos.fecha")
        
        db.partidos.create_index([('torneo_id', 1)])
        print("✓ Índice en partidos.torneo_id")
        
        # Índices en incidencias
        db.incidencias.create_index([('partido_id', 1)])
        print("✓ Índice en incidencias.partido_id")
        
        db.incidencias.create_index([('jugadora_id', 1)])
        print("✓ Índice en incidencias.jugadora_id")
        
        # Índices en noticias
        db.noticias.create_index([('fecha', -1)])
        print("✓ Índice en noticias.fecha")
        
        print("\n✅ Todos los índices de MongoDB han sido creados correctamente.")


if __name__ == "__main__":
    try:
        setup_indexes()
    except Exception as e:
        print(f"\n❌ Error al crear índices: {e}")
        sys.exit(1)
