"""
Crear un usuario en MongoDB asociado (opcionalmente) a un club existente.

Uso (PowerShell en Windows):

  python scripts/crear_usuario_generico.py --username CuadroNacional.sr --password 123456 --club "Cuadro Nacional"

Notas:
- Si el club no existe y pasas --club, se creará automáticamente.
- Si no pasas --club, el usuario se creará sin asociación a club (operador genérico).
"""

import argparse
from app import app
from app.models.usuario import Usuario
from app.models.club import Club
from app.repositories.usuario_repositorio import UsuarioRepositorio
from app.repositories.club_repositorio import ClubRepository
from app.services.usuario_service import UsuarioService


def crear_usuario(username: str, password: str, club_nombre: str | None = None,
                  is_operador: bool = False,
                  puede_cargar_incidencias: bool = False,
                  puede_precargar_equipos: bool = False) -> None:
    """Crea un usuario con contraseña hasheada; opcionalmente lo asocia a un club por nombre."""
    with app.app_context():
        if not username or not password:
            print("ERROR: username y password son obligatorios")
            return

        # Si se especifica club, buscarlo o crearlo
        club_id = None
        if club_nombre:
            club = ClubRepository.buscar_por_nombre(club_nombre)
            if not club:
                club = Club(nombre=club_nombre)
                club = ClubRepository.crear(club)
                print(f"Club creado: {club.nombre} (id={club._id})")
            club_id = club._id

        # Evitar duplicados
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
            is_operador=is_operador,
            puede_cargar_incidencias=puede_cargar_incidencias,
            puede_precargar_equipos=puede_precargar_equipos,
        )
        usuario = UsuarioRepositorio.crear(usuario)
        print(
            f"Usuario '{username}' creado (id={usuario._id})"
            + (f" para el club '{club_nombre}' (id={club_id})" if club_id else " sin club")
        )


def main():
    parser = argparse.ArgumentParser(description="Crear usuario para login de clubes")
    parser.add_argument("--username", required=True, help="Nombre de usuario (p.ej., CuadroNacional.sr)")
    parser.add_argument("--password", required=True, help="Contraseña en texto plano (se guardará hasheada)")
    parser.add_argument("--club", required=False, help="Nombre exacto del club para asociar (opcional)")
    parser.add_argument("--operador", action="store_true", help="Marcar como operador general (sin club)")
    parser.add_argument("--puede-cargar-incidencias", action="store_true", help="Permiso para cargar incidencias")
    parser.add_argument("--puede-precargar-equipos", action="store_true", help="Permiso para precargar equipos")

    args = parser.parse_args()
    crear_usuario(
        username=args.username,
        password=args.password,
        club_nombre=args.club,
        is_operador=bool(args.operador),
        puede_cargar_incidencias=bool(args.puede_cargar_incidencias),
        puede_precargar_equipos=bool(args.puede_precargar_equipos),
    )


if __name__ == "__main__":
    main()