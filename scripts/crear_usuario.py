from app import app, db
from app.models.usuario import Usuario
from app.models.club import Club
from app.services.usuario_service import UsuarioService

# Configura aquí los datos del nuevo usuario y club
def crear_usuario(username, password, nombre_club):
    with app.app_context():
        # Buscar o crear el club
        club = Club.query.filter_by(nombre=nombre_club).first()
        if not club:
            club = Club(nombre=nombre_club)
            db.session.add(club)
            db.session.commit()
        # Crear usuario
        if Usuario.query.filter_by(username=username).first():
            print(f"El usuario '{username}' ya existe.")
            return
        ok, msg = UsuarioService.validar_password(password)
        if not ok:
            print(f"ERROR: {msg}")
            return
        hashed_pw = UsuarioService.hashear_password(password)
        usuario = Usuario(username=username, password=hashed_pw, club_id=club.id)
        db.session.add(usuario)
        db.session.commit()
        print(f"Usuario '{username}' creado para el club '{nombre_club}' (id={club.id})")

# Ejemplo de uso:
# crear_usuario('usuario2', '123456', 'Club Nuevo')

if __name__ == '__main__':
    # Crear usuario Ateneo.sr para el club Ateneo
    crear_usuario('Ateneo.sr', '123456', 'Ateneo')
