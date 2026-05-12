from app.repositories.usuario_repositorio import UsuarioRepositorio
from app.extensions import mongo
from app.models.usuario import Usuario
from app.models.club import Club
from app.repositories.club_repositorio import ClubRepository
from werkzeug.security import check_password_hash, generate_password_hash
from bson import ObjectId
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
            doc = mongo.db.clubes.find_one({'nombre': club_nombre})
            if not doc:
                club = Club(nombre=club_nombre)
                ClubRepository.crear(club)
                club_id = club._id
            else:
                club_id = doc['_id']

        usuario = Usuario(
            username=username,
            password=hashed_pw,
            club_id=club_id,
            is_operador=is_operador,
            puede_cargar_incidencias=puede_cargar_incidencias,
            puede_precargar_equipos=puede_precargar_equipos,
        )
        doc = usuario.to_dict()
        doc.pop('_id', None)
        result = mongo.db.usuarios.insert_one(doc)
        usuario._id = result.inserted_id
        return usuario

    @staticmethod
    def eliminar_usuario(usuario_id) -> bool:
        result = mongo.db.usuarios.delete_one({'_id': ObjectId(usuario_id)})
        return result.deleted_count > 0

    @staticmethod
    def actualizar_usuario_operador(usuario_id, payload: dict) -> Usuario:
        """Actualiza username y/o contraseña de un usuario operador."""
        doc = mongo.db.usuarios.find_one({'_id': ObjectId(usuario_id)})
        if not doc:
            raise ValueError('Usuario no encontrado')
        usuario = Usuario.from_dict(doc)

        nuevo_username = (payload.get('username') or '').strip()
        nuevo_password = payload.get('password') or ''

        update = {}
        if nuevo_username:
            existente = UsuarioRepositorio.buscar_por_username(nuevo_username)
            if existente and existente._id != usuario._id:
                raise ValueError(f"El usuario '{nuevo_username}' ya existe")
            update['username'] = nuevo_username

        if nuevo_password:
            ok, msg = UsuarioService.validar_password(nuevo_password)
            if not ok:
                raise ValueError(msg or 'Contraseña inválida')
            update['password'] = UsuarioService.hashear_password(nuevo_password)

        if update:
            mongo.db.usuarios.update_one(
                {'_id': ObjectId(usuario_id)}, {'$set': update}
            )

        updated_doc = mongo.db.usuarios.find_one({'_id': ObjectId(usuario_id)})
        return Usuario.from_dict(updated_doc)
