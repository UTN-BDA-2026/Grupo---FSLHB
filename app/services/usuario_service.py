from app.repositories.usuario_repositorio import UsuarioRepositorio
from app import db
from app.models.usuario import Usuario
from app.models.club import Club
from werkzeug.security import check_password_hash, generate_password_hash
import re

class UsuarioService:
    @staticmethod
    def autenticar(username, password):
        usuario = UsuarioRepositorio.buscar_por_username(username)
        if usuario and check_password_hash(usuario.password, password):
            return usuario
        return None

    @staticmethod
    def validar_password(password: str) -> tuple[bool, str | None]:
        """Validación mínima: solo que no esté vacía."""
        if not password:
            return False, "La contraseña no puede estar vacía."
        return True, None

    @staticmethod
    def hashear_password(password: str) -> str:
        """Usa el algoritmo por defecto de Werkzeug (PBKDF2-SHA256 con sal)."""
        return generate_password_hash(password)

    @staticmethod
    def listar_operadores():
        """Lista usuarios que actúan como mesas de control (is_operador=True)."""
        return UsuarioRepositorio.listar_operadores()

    @staticmethod
    def crear_operador_desde_payload(payload: dict) -> Usuario:
        """Crea un usuario operador (mesa de control) a partir de datos JSON.

        Espera al menos username y password. club_nombre es opcional.
        """
        username = (payload.get('username') or '').strip()
        password = payload.get('password') or ''
        club_nombre = (payload.get('club_nombre') or '').strip() or None
        is_operador = bool(payload.get('is_operador', True))
        puede_cargar_incidencias = bool(payload.get('puede_cargar_incidencias', True))
        puede_precargar_equipos = bool(payload.get('puede_precargar_equipos', True))

        if not username or not password:
            raise ValueError('username y password son obligatorios')

        # Evitar duplicados
        if UsuarioRepositorio.buscar_por_username(username):
            raise ValueError(f"El usuario '{username}' ya existe")

        ok, msg = UsuarioService.validar_password(password)
        if not ok:
            raise ValueError(msg or 'Contraseña inválida')

        hashed_pw = UsuarioService.hashear_password(password)

        club_id = None
        if club_nombre:
            club = Club.query.filter_by(nombre=club_nombre).first()
            if not club:
                club = Club(nombre=club_nombre)
                db.session.add(club)
                db.session.commit()
            club_id = club.id

        usuario = Usuario(
            username=username,
            password=hashed_pw,
            club_id=club_id,
            is_operador=is_operador,
            puede_cargar_incidencias=puede_cargar_incidencias,
            puede_precargar_equipos=puede_precargar_equipos,
        )
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def eliminar_usuario(usuario_id: int) -> bool:
        usuario = Usuario.query.get(int(usuario_id))
        if not usuario:
            return False
        db.session.delete(usuario)
        db.session.commit()
        return True

    @staticmethod
    def actualizar_usuario_operador(usuario_id: int, payload: dict) -> Usuario:
        """Actualiza username y/o contraseña de un usuario operador."""
        usuario = Usuario.query.get(int(usuario_id))
        if not usuario:
            raise ValueError('Usuario no encontrado')

        nuevo_username = (payload.get('username') or '').strip()
        nuevo_password = payload.get('password') or ''

        if nuevo_username:
            existente = UsuarioRepositorio.buscar_por_username(nuevo_username)
            if existente and existente.id != usuario.id:
                raise ValueError(f"El usuario '{nuevo_username}' ya existe")
            usuario.username = nuevo_username

        if nuevo_password:
            ok, msg = UsuarioService.validar_password(nuevo_password)
            if not ok:
                raise ValueError(msg or 'Contraseña inválida')
            usuario.password = UsuarioService.hashear_password(nuevo_password)

        db.session.commit()
        return usuario
