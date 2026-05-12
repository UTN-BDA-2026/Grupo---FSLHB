from bson import ObjectId
from app.extensions import mongo
from app.models.cuerpo_tecnico import CuerpoTecnico


class CuerpoTecnicoRepositorio:
    @staticmethod
    def _col():
        return mongo.db.cuerpo_tecnico

    @staticmethod
    def crear(data):
        ct = CuerpoTecnico(**data)
        doc = ct.to_dict()
        doc.pop('_id', None)
        result = CuerpoTecnicoRepositorio._col().insert_one(doc)
        ct._id = result.inserted_id
        return ct

    @staticmethod
    def listar(club_id=None):
        query = {'rol': {'$ne': 'ARB'}}
        if club_id:
            query['club_id'] = ObjectId(club_id)
        docs = CuerpoTecnicoRepositorio._col().find(query).sort('_id', 1)
        return [CuerpoTecnico.from_dict(d) for d in docs]

    @staticmethod
    def eliminar(id):
        result = CuerpoTecnicoRepositorio._col().delete_one({'_id': ObjectId(id)})
        return result.deleted_count > 0

    @staticmethod
    def actualizar(id, data):
        result = CuerpoTecnicoRepositorio._col().update_one(
            {'_id': ObjectId(id)}, {'$set': data}
        )
        if result.matched_count == 0:
            return None
        doc = CuerpoTecnicoRepositorio._col().find_one({'_id': ObjectId(id)})
        return CuerpoTecnico.from_dict(doc)
