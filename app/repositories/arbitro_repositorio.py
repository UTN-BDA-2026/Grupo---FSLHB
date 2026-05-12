from bson import ObjectId
from app.extensions import mongo
from app.models.arbitro import Arbitro


class ArbitroRepositorio:
    @staticmethod
    def _col():
        return mongo.db.arbitros

    @staticmethod
    def crear(data: dict):
        arb = Arbitro(**data)
        doc = arb.to_dict()
        doc.pop('_id', None)
        result = ArbitroRepositorio._col().insert_one(doc)
        arb._id = result.inserted_id
        return arb

    @staticmethod
    def obtener(id):
        doc = ArbitroRepositorio._col().find_one({'_id': ObjectId(id)})
        return Arbitro.from_dict(doc)

    @staticmethod
    def listar():
        docs = ArbitroRepositorio._col().find().sort([('apellido', 1), ('nombre', 1)])
        return [Arbitro.from_dict(d) for d in docs]

    @staticmethod
    def eliminar(id) -> bool:
        result = ArbitroRepositorio._col().delete_one({'_id': ObjectId(id)})
        return result.deleted_count > 0

    @staticmethod
    def actualizar(id, nombre=None, apellido=None):
        update = {}
        if nombre is not None:
            update['nombre'] = nombre
        if apellido is not None:
            update['apellido'] = apellido
        if not update:
            return ArbitroRepositorio.obtener(id)
        result = ArbitroRepositorio._col().update_one(
            {'_id': ObjectId(id)}, {'$set': update}
        )
        if result.matched_count == 0:
            return None
        return ArbitroRepositorio.obtener(id)
