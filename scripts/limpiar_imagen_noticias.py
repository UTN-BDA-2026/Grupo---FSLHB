import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db
from app.models.noticia import Noticia
import re

def limpiar_nombre_imagen(ruta):
    # Extrae solo el nombre del archivo de la ruta
    return re.sub(r'.*[\\/]', '', ruta)

with app.app_context():
    noticias = Noticia.query.all()
    for noticia in noticias:
        if noticia.imagen:
            nombre = limpiar_nombre_imagen(noticia.imagen)
            if noticia.imagen != nombre:
                print(f"Corrigiendo: {noticia.imagen} -> {nombre}")
                noticia.imagen = nombre
    db.session.commit()
    print("Imágenes corregidas.")
