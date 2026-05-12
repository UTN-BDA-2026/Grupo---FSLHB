from bson import ObjectId
from app.extensions import mongo
from app.models.incidencia import Incidencia


class IncidenciaRepository:
    @staticmethod
    def _col():
        return mongo.db.incidencias

    @staticmethod
    def crear(inc):
        doc = inc.to_dict()
        doc.pop('_id', None)
        result = IncidenciaRepository._col().insert_one(doc)
        inc._id = result.inserted_id
        return inc

    @staticmethod
    def listar_por_partido(partido_id):
        docs = IncidenciaRepository._col().find(
            {'partido_id': ObjectId(partido_id)}
        ).sort('created_at', 1)
        return [Incidencia.from_dict(d) for d in docs]

    @staticmethod
    def listar_goles_por_partidos(partido_ids):
        if not partido_ids:
            return []
        oids = [ObjectId(pid) for pid in partido_ids]
        docs = IncidenciaRepository._col().find(
            {'partido_id': {'$in': oids}, 'tipo': 'gol'}
        )
        return [Incidencia.from_dict(d) for d in docs]

    @staticmethod
    def max_created_at_por_partido(partido_ids):
        if not partido_ids:
            return {}
        oids = [ObjectId(pid) for pid in partido_ids]
        pipeline = [
            {'$match': {'partido_id': {'$in': oids}}},
            {'$group': {'_id': '$partido_id', 'max_dt': {'$max': '$created_at'}}}
        ]
        rows = IncidenciaRepository._col().aggregate(pipeline)
        return {r['_id']: r['max_dt'] for r in rows}

    @staticmethod
    def ranking_resumen(torneo=None, categoria=None, fecha_hasta=None):
        # First get matching partido IDs
        partido_query = {}
        if torneo:
            partido_query['torneo'] = torneo
        if categoria:
            partido_query['categoria'] = categoria
        if fecha_hasta is not None:
            try:
                fh = int(fecha_hasta)
                partido_query['$or'] = [
                    {'fecha_numero': None},
                    {'fecha_numero': {'$lte': fh}}
                ]
            except Exception:
                pass

        from app.extensions import mongo as _mongo
        partido_ids = [
            d['_id'] for d in _mongo.db.partidos.find(partido_query, {'_id': 1})
        ]
        if not partido_ids:
            return []
        docs = IncidenciaRepository._col().find(
            {'partido_id': {'$in': partido_ids}}
        )
        return [Incidencia.from_dict(d) for d in docs]

    @staticmethod
    def eliminar(partido_id, incidencia_id):
        result = IncidenciaRepository._col().delete_one(
            {'_id': ObjectId(incidencia_id), 'partido_id': ObjectId(partido_id)}
        )
        return result.deleted_count > 0

    @staticmethod
    def listar_tarjetas_por_jugadora(jugadora_id):
        docs = IncidenciaRepository._col().find(
            {'jugadora_id': ObjectId(jugadora_id), 'tipo': 'tarjeta'}
        ).sort('created_at', 1)
        return [Incidencia.from_dict(d) for d in docs]

    @staticmethod
    def eliminar_por_id(incidencia_id):
        result = IncidenciaRepository._col().delete_one(
            {'_id': ObjectId(incidencia_id)}
        )
        return result.deleted_count > 0
