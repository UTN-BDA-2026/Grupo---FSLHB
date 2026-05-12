from bson import ObjectId
from app.extensions import mongo
from app.models.precarga import PrecargaJugadora
from app.models.jugadora import Jugadora


class PrecargaRepository:
    @staticmethod
    def _col():
        return mongo.db.precarga_jugadoras

    @staticmethod
    def listar(partido_id, club_id):
        docs = PrecargaRepository._col().find({
            'partido_id': ObjectId(partido_id),
            'club_id': ObjectId(club_id)
        })
        return [PrecargaJugadora.from_dict(d) for d in docs]

    @staticmethod
    def guardar_lista(partido_id, club_id, jugadora_ids):
        pid = ObjectId(partido_id)
        cid = ObjectId(club_id)
        # Eliminar actuales
        PrecargaRepository._col().delete_many({'partido_id': pid, 'club_id': cid})
        # Crear nuevas
        for jid in jugadora_ids:
            PrecargaRepository._col().insert_one({
                'partido_id': pid,
                'club_id': cid,
                'jugadora_id': ObjectId(jid),
            })
        return True

    @staticmethod
    def listar_con_detalle_por_partido(partido_id):
        pid = ObjectId(partido_id)
        # Obtener precargas
        precargas = list(PrecargaRepository._col().find({'partido_id': pid}))
        if not precargas:
            return {}

        # Obtener jugadoras referenciadas
        jugadora_ids = [p['jugadora_id'] for p in precargas]
        jugadoras_docs = {
            d['_id']: d
            for d in mongo.db.jugadoras.find({'_id': {'$in': jugadora_ids}})
        }

        result = {}
        for p in precargas:
            cid = p['club_id']
            jug = jugadoras_docs.get(p['jugadora_id'], {})
            result.setdefault(cid, []).append({
                'id': jug.get('_id'),
                'nombre': jug.get('nombre', ''),
                'apellido': jug.get('apellido', ''),
                'dni': jug.get('dni'),
                'categoria': jug.get('categoria'),
            })

        # Ordenar cada lista por apellido, nombre
        for cid in result:
            result[cid].sort(key=lambda x: (x['apellido'], x['nombre']))

        return result
