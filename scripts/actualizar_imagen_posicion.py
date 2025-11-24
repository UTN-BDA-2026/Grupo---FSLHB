import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db
from app.models.noticia import Noticia

# Cambia el valor de la imagen para la noticia con el título específico
titulo_objetivo = "Hockey Acción: así están las posiciones"
nueva_ruta = "static/assets/img/Posicion.png"

with app.app_context():
    noticia = Noticia.query.filter_by(titulo=titulo_objetivo).first()
    if noticia:
        noticia.imagen = nueva_ruta
        db.session.commit()
        print(f"Imagen actualizada para: {titulo_objetivo}")
    else:
        print("No se encontró la noticia con ese título.")
