from bson import ObjectId
from app.extensions import mongo
from app.models.club import Club


class ClubRepository:
    @staticmethod
    def _col():
        return mongo.db.clubes
    
    @staticmethod
    def _parse_id(id):
        """Convierte ID numérico a ObjectId o valida ObjectId hexadecimal."""
        # Si es un número, busca el n-ésimo club (1-indexed)
        if isinstance(id, int) or (isinstance(id, str) and id.isdigit()):
            idx = int(id) - 1  # Convertir a 0-indexed
            if idx < 0:
                raise ValueError(f"Índice inválido: {id}")
            docs = ClubRepository._col().find()
            for i, doc in enumerate(docs):
                if i == idx:
                    return doc['_id']
            raise ValueError(f"Club con índice {id} no encontrado")
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
    def crear(club):
        doc = club.to_dict()
        doc.pop('_id', None)
        result = ClubRepository._col().insert_one(doc)
        club._id = result.inserted_id
        return club

    @staticmethod
    def buscar_por_id(id):
        obj_id = ClubRepository._parse_id(id)
        doc = ClubRepository._col().find_one({'_id': obj_id})
        return Club.from_dict(doc)

    @staticmethod
    def buscar_todos():
        docs = ClubRepository._col().find()
        return [Club.from_dict(d) for d in docs]

    @staticmethod
    def actualizar_club(club):
        doc = club.to_dict()
        obj_id = doc.pop('_id', None)
        result = ClubRepository._col().update_one(
            {'_id': obj_id}, {'$set': doc}
        )
        if result.matched_count == 0:
            return None
        return club

    @staticmethod
    def asignar_arbitro(club_id, arbitro_id):
        obj_id = ClubRepository._parse_id(club_id)
        result = ClubRepository._col().update_one(
            {'_id': obj_id},
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
        obj_id = ClubRepository._parse_id(id)
        ClubRepository._col().delete_one({'_id': obj_id})
        return club

    @staticmethod
    def buscar_por_nombre(nombre):
        """Busca un club por nombre."""
        doc = ClubRepository._col().find_one({'nombre': nombre})
        return Club.from_dict(doc)
