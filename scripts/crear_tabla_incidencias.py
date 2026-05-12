"""
Script legacy para inicialización de tablas SQL.

Con MongoDB, las colecciones se crean automáticamente al insertar documentos.
Este script ya no es necesario.

Si necesitas inicializar índices de MongoDB, usa setup_mongodb_indexes.py
"""

from app import app

if __name__ == "__main__":
    with app.app_context():
        print("✓ Aplicación inicializada (MongoDB crea colecciones automáticamente)")
        print("  Para crear índices, ejecuta: python scripts/setup_mongodb_indexes.py")
