import re
from bson import ObjectId
from app.extensions import mongo
from app.models.partido import Partido


class PartidoRepository:
    @staticmethod
    def _col():
        return mongo.db.partidos

    @staticmethod
    def puede_agregar_fecha(torneo_nombre: str, max_fechas: int) -> bool:
        pipeline = [
            {'$match': {'torneo': torneo_nombre}},
            {'$group': {'_id': '$fecha_numero'}},
            {'$count': 'total'}
        ]
        result = list(PartidoRepository._col().aggregate(pipeline))
        fechas_jugadas = result[0]['total'] if result else 0
        return fechas_jugadas < max_fechas

    @staticmethod
    def crear(partido):
        doc = partido.to_dict()
        doc.pop('_id', None)
        result = PartidoRepository._col().insert_one(doc)
        partido._id = result.inserted_id
        return partido

    @staticmethod
    def buscar_por_id(id):
        doc = PartidoRepository._col().find_one({'_id': ObjectId(id)})
        return Partido.from_dict(doc)

    @staticmethod
    def buscar(filtros: dict):
        query = {}
        if filtros.get('torneo'):
            query['torneo'] = {'$regex': re.escape(filtros['torneo']), '$options': 'i'}
        if filtros.get('categoria'):
            query['categoria'] = {'$regex': re.escape(filtros['categoria']), '$options': 'i'}
        if filtros.get('club_id'):
            cid = filtros['club_id']
            query['$or'] = [{'club_local_id': cid}, {'club_visitante_id': cid}]
        if filtros.get('fecha_numero'):
            query['fecha_numero'] = filtros['fecha_numero']
        if filtros.get('estado'):
            query['estado'] = {'$regex': f'^{re.escape(filtros["estado"])}$', '$options': 'i'}
        if filtros.get('estado_not'):
            query['estado'] = {'$ne': filtros['estado_not']}

        docs = PartidoRepository._col().find(query).sort('fecha_hora', 1)
        return [Partido.from_dict(d) for d in docs]

    @staticmethod
    def actualizar(partido):
        doc = partido.to_dict()
        doc.pop('_id', None)
        PartidoRepository._col().update_one(
            {'_id': ObjectId(partido._id)}, {'$set': doc}
        )
        return partido

    @staticmethod
    def eliminar(partido):
        PartidoRepository._col().delete_one({'_id': ObjectId(partido._id)})
