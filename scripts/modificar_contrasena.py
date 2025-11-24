from app import app, db
from app.models.usuario import Usuario
from app.services.usuario_service import UsuarioService

def modificar_contrasena(username, nueva_contrasena):
    with app.app_context():
        usuario = Usuario.query.filter_by(username=username).first()
        if not usuario:
            print(f"No existe el usuario '{username}'.")
            return
        ok, msg = UsuarioService.validar_password(nueva_contrasena)
        if not ok:
            print(f"ERROR: {msg}")
            return
        usuario.password = UsuarioService.hashear_password(nueva_contrasena)
        db.session.commit()
        print(f"Contraseña modificada para el usuario '{username}'.")

# Ejemplo de uso:
# modificar_contrasena('Fenix.sr', 'nueva123')

if __name__ == '__main__':
    # Cambia estos valores para el usuario y la nueva contraseña
    modificar_contrasena('Fenix.sr', 'nueva123')
