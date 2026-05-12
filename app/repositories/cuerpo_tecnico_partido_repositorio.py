from bson import ObjectId
from app.extensions import mongo
from app.models.cuerpo_tecnico_partido import CuerpoTecnicoPartido


class CuerpoTecnicoPartidoRepositorio:
    @staticmethod
    def _col():
        return mongo.db.cuerpo_tecnico_partido

    @staticmethod
    def upsert(partido_id, club_id, rol, cuerpo_tecnico_id):
        pid = ObjectId(partido_id)
        cid = ObjectId(club_id)
        ct_id = ObjectId(cuerpo_tecnico_id)

        existente = CuerpoTecnicoPartidoRepositorio._col().find_one(
            {'partido_id': pid, 'club_id': cid, 'rol': rol}
        )
        if existente:
            CuerpoTecnicoPartidoRepositorio._col().update_one(
                {'_id': existente['_id']},
                {'$set': {'cuerpo_tecnico_id': ct_id}}
            )
            doc = CuerpoTecnicoPartidoRepositorio._col().find_one({'_id': existente['_id']})
        else:
            new_doc = {
                'partido_id': pid,
                'club_id': cid,
                'rol': rol,
                'cuerpo_tecnico_id': ct_id,
            }
            result = CuerpoTecnicoPartidoRepositorio._col().insert_one(new_doc)
            doc = CuerpoTecnicoPartidoRepositorio._col().find_one({'_id': result.inserted_id})
        return CuerpoTecnicoPartido.from_dict(doc)

    @staticmethod
    def listar_por_partido(partido_id):
        docs = CuerpoTecnicoPartidoRepositorio._col().find(
            {'partido_id': ObjectId(partido_id)}
        )
        return [CuerpoTecnicoPartido.from_dict(d) for d in docs]
