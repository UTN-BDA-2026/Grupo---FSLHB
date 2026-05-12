from bson import ObjectId
from app.extensions import mongo
from app.models.usuario import Usuario


class UsuarioRepositorio:
    @staticmethod
    def _col():
        return mongo.db.usuarios

    @staticmethod
    def buscar_por_username(username):
        doc = UsuarioRepositorio._col().find_one({'username': username})
        return Usuario.from_dict(doc)

    @staticmethod
    def buscar_por_id(user_id):
        doc = UsuarioRepositorio._col().find_one({'_id': ObjectId(user_id)})
        return Usuario.from_dict(doc)

    @staticmethod
    def listar_operadores():
        """Devuelve los usuarios que actúan como mesas de control.

        Se consideran mesas de control aquellos usuarios que sean operadores
        generales o tengan permisos especiales de incidencias o precarga.
        """
        docs = UsuarioRepositorio._col().find({
            '$or': [
                {'is_operador': True},
                {'puede_cargar_incidencias': True},
                {'puede_precargar_equipos': True},
            ]
        })
        return [Usuario.from_dict(d) for d in docs]

    @staticmethod
    def crear(usuario):
        """Crea un nuevo usuario en MongoDB."""
        doc = usuario.to_dict()
        doc.pop('_id', None)
        result = UsuarioRepositorio._col().insert_one(doc)
        usuario._id = result.inserted_id
        return usuario

    @staticmethod
    def actualizar(usuario):
        """Actualiza un usuario existente en MongoDB."""
        doc = usuario.to_dict()
        doc.pop('_id', None)
        result = UsuarioRepositorio._col().update_one(
            {'_id': ObjectId(usuario._id)}, {'$set': doc}
        )
        if result.matched_count == 0:
            return None
        return usuario
