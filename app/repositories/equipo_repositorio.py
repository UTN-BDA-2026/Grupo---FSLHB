import re
from bson import ObjectId
from app.extensions import mongo
from app.models.equipo import Equipo


class EquipoRepository:
    @staticmethod
    def _col():
        return mongo.db.equipos

    @staticmethod
    def crear(equipo):
        doc = equipo.to_dict()
        doc.pop('_id', None)
        result = EquipoRepository._col().insert_one(doc)
        equipo._id = result.inserted_id
        return equipo

    @staticmethod
    def buscar_por_id(id):
        doc = EquipoRepository._col().find_one({'_id': ObjectId(id)})
        return Equipo.from_dict(doc)

    @staticmethod
    def buscar_todos():
        docs = EquipoRepository._col().find()
        return [Equipo.from_dict(d) for d in docs]

    @staticmethod
    def buscar_por_club(club_id):
        docs = EquipoRepository._col().find({'club_id': ObjectId(club_id)})
        return [Equipo.from_dict(d) for d in docs]

    @staticmethod
    def buscar_por_categoria(categoria):
        if not categoria:
            return EquipoRepository.buscar_todos()
        docs = EquipoRepository._col().find({
            'categoria': {'$regex': re.escape(categoria), '$options': 'i'}
        })
        return [Equipo.from_dict(d) for d in docs]

    @staticmethod
    def actualizar_equipo(equipo):
        doc = equipo.to_dict()
        doc.pop('_id', None)
        result = EquipoRepository._col().update_one(
            {'_id': ObjectId(equipo._id)}, {'$set': doc}
        )
        if result.matched_count == 0:
            return None
        return equipo

    @staticmethod
    def borrar_por_id(id):
        equipo = EquipoRepository.buscar_por_id(id)
        if not equipo:
            return None
        EquipoRepository._col().delete_one({'_id': ObjectId(id)})
        return equipo
