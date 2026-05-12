from app.models.incidencia import Incidencia
from app.repositories.incidencia_repositorio import IncidenciaRepository
from app.extensions import mongo
from bson import ObjectId


class IncidenciaService:
    @staticmethod
    def registrar_gol(partido_id, club_id, jugadora_id, minuto=None):
        inc = Incidencia(
            partido_id=ObjectId(partido_id),
            club_id=ObjectId(club_id),
            jugadora_id=ObjectId(jugadora_id),
            tipo='gol',
            minuto=minuto
        )
        return IncidenciaRepository.crear(inc)

    @staticmethod
    def registrar_tarjeta(partido_id, club_id, jugadora_id, color, minuto=None):
        inc = Incidencia(
            partido_id=ObjectId(partido_id),
            club_id=ObjectId(club_id),
            jugadora_id=ObjectId(jugadora_id),
            tipo='tarjeta',
            color=color,
            minuto=minuto
        )
        return IncidenciaRepository.crear(inc)

    @staticmethod
    def listar(partido_id):
        return IncidenciaRepository.listar_por_partido(partido_id)

    @staticmethod
    def registrar_lesion(partido_id, club_id, jugadora_id, minuto=None):
        inc = Incidencia(
            partido_id=ObjectId(partido_id),
            club_id=ObjectId(club_id),
            jugadora_id=ObjectId(jugadora_id),
            tipo='lesion',
            minuto=minuto
        )
        return IncidenciaRepository.crear(inc)

    @staticmethod
    def listar_goles_por_partidos(partido_ids):
        return IncidenciaRepository.listar_goles_por_partidos(partido_ids)

    @staticmethod
    def listar_tarjetas_por_partidos(partido_ids, color=None):
        if not partido_ids:
            return []
        oids = [ObjectId(pid) for pid in partido_ids]
        query = {'partido_id': {'$in': oids}, 'tipo': 'tarjeta'}
        if color:
            query['color'] = color
        docs = mongo.db.incidencias.find(query)
        return [Incidencia.from_dict(d) for d in docs]

    @staticmethod
    def ranking_resumen(torneo=None, categoria=None, fecha_hasta=None):
        return IncidenciaRepository.ranking_resumen(torneo, categoria, fecha_hasta)

    @staticmethod
    def eliminar(partido_id, incidencia_id):
        return IncidenciaRepository.eliminar(partido_id, incidencia_id)

    @staticmethod
    def listar_tarjetas_por_jugadora(jugadora_id):
        return IncidenciaRepository.listar_tarjetas_por_jugadora(jugadora_id)

    @staticmethod
    def eliminar_por_id(incidencia_id):
        return IncidenciaRepository.eliminar_por_id(incidencia_id)
