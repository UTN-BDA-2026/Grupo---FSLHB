from bson import ObjectId
from app.extensions import mongo
from app.models.club import Club


class ClubRepository:
    @staticmethod
    def _col():
        return mongo.db.clubes

    @staticmethod
    def crear(club):
        doc = club.to_dict()
        doc.pop('_id', None)
        result = ClubRepository._col().insert_one(doc)
        club._id = result.inserted_id
        return club

    @staticmethod
    def buscar_por_id(id):
        doc = ClubRepository._col().find_one({'_id': ObjectId(id)})
        return Club.from_dict(doc)

    @staticmethod
    def buscar_todos():
        docs = ClubRepository._col().find()
        return [Club.from_dict(d) for d in docs]

    @staticmethod
    def actualizar_club(club):
        doc = club.to_dict()
        doc.pop('_id', None)
        result = ClubRepository._col().update_one(
            {'_id': ObjectId(club._id)}, {'$set': doc}
        )
        if result.matched_count == 0:
            return None
        return club

    @staticmethod
    def asignar_arbitro(club_id, arbitro_id):
        result = ClubRepository._col().update_one(
            {'_id': ObjectId(club_id)},
            {'$set': {'arbitro_id': arbitro_id}}
        )
        if result.matched_count == 0:
            return None
        return ClubRepository.buscar_por_id(club_id)

    @staticmethod
    def borrar_por_id(id):
        club = ClubRepository.buscar_por_id(id)
        if not club:
            return None
        ClubRepository._col().delete_one({'_id': ObjectId(id)})
        return club
