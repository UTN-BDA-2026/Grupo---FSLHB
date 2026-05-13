"""Migración simple: jugadoras desde MongoDB hacia MariaDB.

- Lee documentos de `mongo.db.jugadoras`
- Inserta filas en MariaDB (SQLAlchemy) en tabla `jugadoras`
- Evita duplicados por DNI cuando existe

Uso (dentro del contenedor app o en local con env vars):
  python scripts/migrate_jugadoras_mongo_to_mariadb.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Permite ejecutar el script como archivo (python scripts/...) dentro de Docker,
# agregando el root del repo a sys.path para poder importar el paquete `app`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def _to_str(value) -> str | None:
    if value is None:
        return None
    s = str(value).strip()
    return s or None


def main() -> None:
    from app.factory import create_app
    from app.extensions import db, mongo
    from app.models.jugadora import Jugadora

    app = create_app()

    with app.app_context():
        db.create_all()

        total = 0
        created = 0
        skipped = 0

        for doc in mongo.db.jugadoras.find({}):
            total += 1

            dni = _to_str(doc.get("dni"))
            if dni and Jugadora.query.filter_by(dni=dni).first() is not None:
                skipped += 1
                continue

            jugadora = Jugadora(
                nombre=_to_str(doc.get("nombre")) or "",
                apellido=_to_str(doc.get("apellido")) or "",
                dni=dni,
                fecha_nacimiento=_to_str(doc.get("fecha_nacimiento")),
                categoria=_to_str(doc.get("categoria")),
                club_id=_to_str(doc.get("club_id")) or "",
            )
            db.session.add(jugadora)
            created += 1

        db.session.commit()

        print(
            f"Mongo->MariaDB jugadoras: total={total} created={created} skipped={skipped}"
        )


if __name__ == "__main__":
    main()
