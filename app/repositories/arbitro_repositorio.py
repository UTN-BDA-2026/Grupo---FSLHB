from bson import ObjectId
from app.extensions import mongo
from app.models.arbitro import Arbitro


class ArbitroRepositorio:
    @staticmethod
    def _col():
        return mongo.db.arbitros
    
    @staticmethod
    def _parse_id(id):
        """Convierte ID numérico a ObjectId o valida ObjectId hexadecimal."""
        # Si es un número, busca el n-ésimo árbitro (1-indexed)
        if isinstance(id, int) or (isinstance(id, str) and id.isdigit()):
            idx = int(id) - 1  # Convertir a 0-indexed
            if idx < 0:
                raise ValueError(f"Índice inválido: {id}")
            docs = ArbitroRepositorio._col().find().sort([('apellido', 1), ('nombre', 1)])
            for i, doc in enumerate(docs):
                if i == idx:
                    return doc['_id']
            raise ValueError(f"Árbitro con índice {id} no encontrado")
        # Si es un string hexadecimal, trátalo como ObjectId
        if isinstance(id, str) and len(id) == 24:
            try:
                return ObjectId(id)
            except:
                raise ValueError(f"ID inválido: {id}")
        # Si es ObjectId, retórnalo
        if isinstance(id, ObjectId):
            return id
        raise ValueError(f"ID inválido: {id}")

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
        obj_id = ArbitroRepositorio._parse_id(id)
        doc = ArbitroRepositorio._col().find_one({'_id': obj_id})
        return Arbitro.from_dict(doc)

    @staticmethod
    def listar():
        docs = ArbitroRepositorio._col().find().sort([('apellido', 1), ('nombre', 1)])
        return [Arbitro.from_dict(d) for d in docs]

    @staticmethod
    def eliminar(id) -> bool:
        obj_id = ArbitroRepositorio._parse_id(id)
        result = ArbitroRepositorio._col().delete_one({'_id': obj_id})
        return result.deleted_count > 0

    @staticmethod
    def actualizar(id, nombre=None, apellido=None):
        obj_id = ArbitroRepositorio._parse_id(id)
        update = {}
        if nombre is not None:
            update['nombre'] = nombre
        if apellido is not None:
            update['apellido'] = apellido
        if not update:
            return ArbitroRepositorio.obtener(id)
        result = ArbitroRepositorio._col().update_one(
            {'_id': obj_id}, {'$set': update}
        )
        if result.matched_count == 0:
            return None
        return ArbitroRepositorio.obtener(id)
