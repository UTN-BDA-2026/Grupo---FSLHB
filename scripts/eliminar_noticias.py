import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db
from app.models.noticia import Noticia

titulos_a_borrar = [
    "Torneo Juvenil: grandes promesas en acción",
]

with app.app_context():
    print("Títulos actuales en la base de datos:")
    for noticia in Noticia.query.all():
        print(f"- {noticia.titulo}")
    print("\nIntentando eliminar:")
    noticias = Noticia.query.filter(Noticia.titulo.in_(titulos_a_borrar)).all()
    for noticia in noticias:
        db.session.delete(noticia)
        print(f"Eliminada: {noticia.titulo}")
    db.session.commit()
    print("Noticias eliminadas correctamente.")
