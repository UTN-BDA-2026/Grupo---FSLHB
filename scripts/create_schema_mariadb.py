"""
Script legacy para crear esquema en MariaDB.

Este proyecto ahora usa MongoDB. Este script ya no es necesario.
Las colecciones de MongoDB se crean automáticamente al insertar documentos.

Para inicializar índices de MongoDB, ejecuta:
  python scripts/setup_mongodb_indexes.py
"""

import os
import sys

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from app import create_app


def main() -> int:
    app = create_app("production")
    with app.app_context():
        print("✓ Proyecto usando MongoDB")
        print("  Colecciones se crean automáticamente")
        print("  Para índices: python scripts/setup_mongodb_indexes.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
