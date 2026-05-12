import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar .env automáticamente
basedir = Path(__file__).resolve().parents[1]
env_path = os.path.join(basedir, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

from app import app
from app.models.usuario import Usuario
from app.models.club import Club
from app.repositories.usuario_repositorio import UsuarioRepositorio
from app.repositories.club_repositorio import ClubRepository
from app.services.usuario_service import UsuarioService

# Configura aquí los datos del nuevo usuario y club
def crear_usuario(username, password, nombre_club):
    with app.app_context():
        # Buscar o crear el club (solo si se especifica)
        club_id = None
        if nombre_club:
            club = ClubRepository.buscar_por_nombre(nombre_club)
            if not club:
                club = Club(nombre=nombre_club)
                club = ClubRepository.crear(club)
        
        # Crear usuario
        if UsuarioRepositorio.buscar_por_username(username):
            print(f"El usuario '{username}' ya existe.")
            return
        
        ok, msg = UsuarioService.validar_password(password)
        if not ok:
            print(f"ERROR: {msg}")
            return
        
        hashed_pw = UsuarioService.hashear_password(password)
        usuario = Usuario(
            username=username, 
            password=hashed_pw, 
            club_id=club_id,
            is_admin=True
        )
        usuario = UsuarioRepositorio.crear(usuario)
        print(f"Usuario admin '{username}' creado (id={usuario._id})")


# Ejemplo de uso:
# crear_usuario('admin', 'ContraseñaSuperSegura!2025', None)

if __name__ == '__main__':
    # Crear usuario admin seguro
    crear_usuario('admin', 'G7!pXr@2vQz#Lw9sTj$e', None)
