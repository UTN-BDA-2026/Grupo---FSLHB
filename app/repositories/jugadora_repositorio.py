from bson import ObjectId
from app.extensions import mongo
from app.models.jugadora import Jugadora


class JugadoraRepository:
    @staticmethod
    def _col():
        return mongo.db.jugadoras

    @staticmethod
    def crear(jugadora):
        doc = jugadora.to_dict()
        doc.pop('_id', None)
        result = JugadoraRepository._col().insert_one(doc)
        jugadora._id = result.inserted_id
        return jugadora

    @staticmethod
    def buscar_por_id(id):
        doc = JugadoraRepository._col().find_one({'_id': ObjectId(id)})
        return Jugadora.from_dict(doc)

    @staticmethod
    def buscar_todas():
        docs = JugadoraRepository._col().find()
        return [Jugadora.from_dict(d) for d in docs]

    @staticmethod
    def buscar_por_club(club_id):
        docs = JugadoraRepository._col().find({'club_id': ObjectId(club_id)})
        return [Jugadora.from_dict(d) for d in docs]

    @staticmethod
    def actualizar_jugadora(jugadora):
        doc = jugadora.to_dict()
        doc.pop('_id', None)
        result = JugadoraRepository._col().update_one(
            {'_id': ObjectId(jugadora._id)}, {'$set': doc}
        )
        if result.matched_count == 0:
            return None
        return jugadora

    @staticmethod
    def borrar_por_id(id):
        jugadora = JugadoraRepository.buscar_por_id(id)
        if not jugadora:
            return None
        JugadoraRepository._col().delete_one({'_id': ObjectId(id)})
        return jugadora
