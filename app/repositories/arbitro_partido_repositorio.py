from bson import ObjectId
from app.extensions import mongo
from app.models.arbitro_partido import ArbitroPartido
from app.models.arbitro import Arbitro


class ArbitroPartidoRepositorio:
    @staticmethod
    def _col():
        return mongo.db.arbitro_partido

    @staticmethod
    def listar_por_partido(partido_id):
        docs = ArbitroPartidoRepositorio._col().find(
            {'partido_id': ObjectId(partido_id)}
        )
        result = []
        for doc in docs:
            ap = ArbitroPartido.from_dict(doc)
            # Cargar el árbitro asociado
            arb_doc = mongo.db.arbitros.find_one({'_id': ObjectId(ap.arbitro_id)})
            arb = Arbitro.from_dict(arb_doc)
            result.append((ap, arb))
        # Ordenar por apellido, nombre del árbitro
        result.sort(key=lambda x: (x[1].apellido if x[1] else '', x[1].nombre if x[1] else ''))
        return result

    @staticmethod
    def set_por_equipo(partido_id, club_id, arbitro_id):
        pid = ObjectId(partido_id)
        cid = ObjectId(club_id) if club_id else None

        existente = ArbitroPartidoRepositorio._col().find_one(
            {'partido_id': pid, 'club_id': cid}
        )

        if arbitro_id is None:
            if existente:
                ArbitroPartidoRepositorio._col().delete_one({'_id': existente['_id']})
            return None

        aid = ObjectId(arbitro_id)
        if existente:
            ArbitroPartidoRepositorio._col().update_one(
                {'_id': existente['_id']},
                {'$set': {'arbitro_id': aid}}
            )
        else:
            ArbitroPartidoRepositorio._col().insert_one({
                'partido_id': pid,
                'club_id': cid,
                'arbitro_id': aid,
            })

        doc = ArbitroPartidoRepositorio._col().find_one(
            {'partido_id': pid, 'club_id': cid}
        )
        return ArbitroPartido.from_dict(doc)
