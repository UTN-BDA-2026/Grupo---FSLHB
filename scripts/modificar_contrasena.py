# Cargar variables de entorno desde .env automáticamente
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print('Advertencia: python-dotenv no está instalado. Variables de entorno del .env pueden no cargarse.')

from app import app
from app.models.usuario import Usuario
from app.repositories.usuario_repositorio import UsuarioRepositorio
from app.services.usuario_service import UsuarioService

def modificar_contrasena(username, nueva_contrasena):
    with app.app_context():
        usuario = UsuarioRepositorio.buscar_por_username(username)
        if not usuario:
            print(f"No existe el usuario '{username}'.")
            return
        ok, msg = UsuarioService.validar_password(nueva_contrasena)
        if not ok:
            print(f"ERROR: {msg}")
            return
        usuario.password = UsuarioService.hashear_password(nueva_contrasena)
        UsuarioRepositorio.actualizar(usuario)
        print(f"Contraseña modificada para el usuario '{username}'.")

# Ejemplo de uso:
# modificar_contrasena('Fenix.sr', 'nueva123')

if __name__ == '__main__':
    # Cambia estos valores para el usuario y la nueva contraseña
    usuario = 'SanJorge.sr'
    nueva_contrasena = 'SanJorge_sr!'
    modificar_contrasena(usuario, nueva_contrasena)
