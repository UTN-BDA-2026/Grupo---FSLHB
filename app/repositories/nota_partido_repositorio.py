from bson import ObjectId
from app.extensions import mongo
from app.models.nota_partido import NotaPartido


class NotaPartidoRepository:
    @staticmethod
    def _col():
        return mongo.db.notas_partido

    @staticmethod
    def obtener_por_partido(partido_id):
        doc = NotaPartidoRepository._col().find_one(
            {'partido_id': ObjectId(partido_id)}
        )
        return NotaPartido.from_dict(doc)

    @staticmethod
    def upsert(partido_id, detalle):
        pid = ObjectId(partido_id)
        nota = NotaPartidoRepository._col().find_one({'partido_id': pid})
        if nota is None:
            new_doc = {'partido_id': pid, 'detalle': detalle}
            result = NotaPartidoRepository._col().insert_one(new_doc)
            doc = NotaPartidoRepository._col().find_one({'_id': result.inserted_id})
        else:
            NotaPartidoRepository._col().update_one(
                {'_id': nota['_id']},
                {'$set': {'detalle': detalle}}
            )
            doc = NotaPartidoRepository._col().find_one({'_id': nota['_id']})
        return NotaPartido.from_dict(doc)
