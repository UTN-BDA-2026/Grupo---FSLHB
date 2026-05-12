import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from app.repositories.noticia_repositorio import NoticiaRepositorio

# Cambia el valor de la imagen para la noticia con el título específico
titulo_objetivo = "Hockey Acción: así están las posiciones"
nueva_ruta = "static/assets/img/Posicion.png"

with app.app_context():
    noticia = NoticiaRepositorio.obtener_por_titulo(titulo_objetivo)
    if noticia:
        noticia.imagen = nueva_ruta
        NoticiaRepositorio.actualizar_noticia(noticia)
        print(f"Imagen actualizada para: {titulo_objetivo}")
    else:
        print("No se encontró la noticia con ese título.")
