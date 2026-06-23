from bson import ObjectId
from app.extensions import mongo
from app.models.torneo import Torneo


class TorneoRepository:
    @staticmethod
    def _col():
        return mongo.db.torneos
    
    @staticmethod
    def _parse_id(id):
        """Convierte ID numérico a ObjectId o valida ObjectId hexadecimal."""
        # Si es un número, busca el n-ésimo torneo (1-indexed)
        if isinstance(id, int) or (isinstance(id, str) and id.isdigit()):
            idx = int(id) - 1  # Convertir a 0-indexed
            if idx < 0:
                raise ValueError(f"Índice inválido: {id}")
            docs = TorneoRepository._col().find().sort('_id', 1)
            for i, doc in enumerate(docs):
                if i == idx:
                    return doc['_id']
            raise ValueError(f"Torneo con índice {id} no encontrado")
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
    def agregar_torneo(nombre, max_fechas):
        doc = {'nombre': nombre, 'max_fechas': max_fechas}
        result = TorneoRepository._col().insert_one(doc)
        return {
            "mensaje": "Torneo agregado",
            "id": str(result.inserted_id),
            "nombre": nombre,
            "max_fechas": max_fechas,
        }

    @staticmethod
    def obtener_torneos():
        docs = TorneoRepository._col().find().sort('_id', 1)
        return [
            {"id": str(t['_id']), "nombre": t['nombre'], "max_fechas": t['max_fechas']}
            for t in docs
        ]

    @staticmethod
    def actualizar_torneo(torneo_id, nombre, max_fechas):
        obj_id = TorneoRepository._parse_id(torneo_id)
        result = TorneoRepository._col().update_one(
            {'_id': obj_id},
            {'$set': {'nombre': nombre, 'max_fechas': max_fechas}}
        )
        if result.matched_count == 0:
            return None
        return {"id": str(obj_id), "nombre": nombre, "max_fechas": max_fechas}

    @staticmethod
    def eliminar_torneo(torneo_id) -> bool:
        obj_id = TorneoRepository._parse_id(torneo_id)
        result = TorneoRepository._col().delete_one({'_id': obj_id})
        return result.deleted_count > 0

    @staticmethod
    def guardar_seleccion(data):
        return {"mensaje": "Selección guardada", "data": data}
