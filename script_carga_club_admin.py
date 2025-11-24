# script_carga_club_admin.py
# Script para cargar un club y un usuario admin asociado en la base de datos

from app import db
from app.models.club import Club
from app.models.usuario import Usuario

# Crear el club
club = Club(
    nombre="SAN RAFAEL TENIS CLUB",
    razon_social="SAN RAFAEL TENIS CLUB",
    contacto="2604413283",
    email="jorgepablof@hotmail.com",
    cancha_local="SAN RAFAEL TENIS CLUB",
    domicilio="SOBREMONTE 737",
    telefono="02604423744",
    web="www.sanrafaeltenisclub.c"
)
db.session.add(club)
db.session.commit()

# Crear el usuario admin asociado a ese club
admin = Usuario(
    username="admin",
    password="admin123",  # Recuerda hashear la contraseña en producción
    nombre="Administrador",
    club_id=club.id,
    es_admin=True
)
db.session.add(admin)
db.session.commit()

print(f"Club y usuario admin creados con éxito. Club ID: {club.id}, Usuario: {admin.username}")
