from app import app, db
from app.models.noticia import Noticia

with app.app_context():
    db.create_all()
    print("Tablas creadas correctamente.")
