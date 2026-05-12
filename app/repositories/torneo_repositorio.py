from bson import ObjectId
from app.extensions import mongo
from app.models.torneo import Torneo


class TorneoRepository:
    @staticmethod
    def _col():
        return mongo.db.torneos

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
        result = TorneoRepository._col().update_one(
            {'_id': ObjectId(torneo_id)},
            {'$set': {'nombre': nombre, 'max_fechas': max_fechas}}
        )
        if result.matched_count == 0:
            return None
        return {"id": str(torneo_id), "nombre": nombre, "max_fechas": max_fechas}

    @staticmethod
    def eliminar_torneo(torneo_id) -> bool:
        result = TorneoRepository._col().delete_one({'_id': ObjectId(torneo_id)})
        return result.deleted_count > 0

    @staticmethod
    def guardar_seleccion(data):
        return {"mensaje": "Selección guardada", "data": data}
