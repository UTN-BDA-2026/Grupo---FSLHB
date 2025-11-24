import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models.noticia import Noticia

# Ruta al archivo JSON de noticias
json_path = os.path.join('src', 'data', 'noticias.json')

with open(json_path, 'r', encoding='utf-8') as f:
    noticias = json.load(f)

with app.app_context():
    for n in noticias:
        noticia = Noticia(
            titulo=n.get('titulo', ''),
            resumen=n.get('resumen', ''),
            contenido=n.get('contenido', ''),
            imagen=n.get('imagen', ''),
            fecha=n.get('fecha', '')
        )
        db.session.add(noticia)
    db.session.commit()
    print(f"Importadas {len(noticias)} noticias correctamente.")
