from app import app, db
from app.models.incidencia import Incidencia  # noqa: F401

# Crea la(s) tabla(s) faltante(s) según los modelos definidos
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Tabla Incidencias creada si no existía.")
