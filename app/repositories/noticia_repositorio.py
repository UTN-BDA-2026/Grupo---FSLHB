from bson import ObjectId
from bson.errors import InvalidId
from app.extensions import mongo
from app.models.noticia import Noticia


class NoticiaRepositorio:
    @staticmethod
    def _col():
        return mongo.db.noticias

    @staticmethod
    def obtener_todas(limit=None):
        cursor = NoticiaRepositorio._col().find().sort('fecha', -1)
        if limit is not None:
            try:
                lim = int(limit)
                if lim > 0:
                    cursor = cursor.limit(lim)
            except (ValueError, TypeError):
                pass
        return [Noticia.from_dict(d) for d in cursor]

    @staticmethod
    def obtener_por_id(noticia_id):
        try:
            oid = ObjectId(noticia_id)
        except (InvalidId, TypeError):
            return None
        doc = NoticiaRepositorio._col().find_one({'_id': oid})
        return Noticia.from_dict(doc)

    @staticmethod
    def crear_noticia(data):
        noticia = Noticia(**data)
        doc = noticia.to_dict()
        doc.pop('_id', None)
        result = NoticiaRepositorio._col().insert_one(doc)
        noticia._id = result.inserted_id
        return noticia

    @staticmethod
    def eliminar_noticia(noticia_id):
        try:
            oid = ObjectId(noticia_id)
        except (InvalidId, TypeError):
            return False
        result = NoticiaRepositorio._col().delete_one({'_id': oid})
        return result.deleted_count > 0

    @staticmethod
    def actualizar_noticia(noticia):
        """Actualiza una noticia existente en MongoDB."""
        doc = noticia.to_dict()
        doc.pop('_id', None)
        result = NoticiaRepositorio._col().update_one(
            {'_id': ObjectId(noticia._id)}, {'$set': doc}
        )
        if result.matched_count == 0:
            return None
        return noticia

    @staticmethod
    def obtener_por_titulo(titulo):
        """Obtiene una noticia por título."""
        doc = NoticiaRepositorio._col().find_one({'titulo': titulo})
        return Noticia.from_dict(doc)
