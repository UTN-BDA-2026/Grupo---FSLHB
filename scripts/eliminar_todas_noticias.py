import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db
from app.models.noticia import Noticia

with app.app_context():
    num = Noticia.query.delete()
    db.session.commit()
    print(f"Eliminadas {num} noticias.")
