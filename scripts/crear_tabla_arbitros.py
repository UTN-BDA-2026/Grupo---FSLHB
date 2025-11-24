from app import app, db
from app.models.arbitro import Arbitro  # noqa: F401
from app.models.arbitro_partido import ArbitroPartido  # noqa: F401

# Crea la(s) tabla(s) faltante(s) según los modelos definidos
# Incluye arbitros y arbitro_partido
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Tablas 'arbitros' y 'arbitro_partido' creadas si no existían.")
