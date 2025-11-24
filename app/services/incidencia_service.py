from app.models.incidencia import Incidencia
from app.repositories.incidencia_repositorio import IncidenciaRepository

class IncidenciaService:
    @staticmethod
    def registrar_gol(partido_id: int, club_id: int, jugadora_id: int, minuto: int | None):
        inc = Incidencia(partido_id=partido_id, club_id=club_id, jugadora_id=jugadora_id, tipo='gol', minuto=minuto)
        return IncidenciaRepository.crear(inc)

    @staticmethod
    def registrar_tarjeta(partido_id: int, club_id: int, jugadora_id: int, color: str, minuto: int | None):
        inc = Incidencia(partido_id=partido_id, club_id=club_id, jugadora_id=jugadora_id, tipo='tarjeta', color=color, minuto=minuto)
        return IncidenciaRepository.crear(inc)

    @staticmethod
    def listar(partido_id: int):
        return IncidenciaRepository.listar_por_partido(partido_id)

    @staticmethod
    def registrar_lesion(partido_id: int, club_id: int, jugadora_id: int, minuto: int | None):
        inc = Incidencia(partido_id=partido_id, club_id=club_id, jugadora_id=jugadora_id, tipo='lesion', minuto=minuto)
        return IncidenciaRepository.crear(inc)

    @staticmethod
    def listar_goles_por_partidos(partido_ids):
        return IncidenciaRepository.listar_goles_por_partidos(partido_ids)

    @staticmethod
    def listar_tarjetas_por_partidos(partido_ids, color=None):
        if not partido_ids:
            return []
        query = Incidencia.query.filter(Incidencia.partido_id.in_(partido_ids), Incidencia.tipo == 'tarjeta')
        if color:
            query = query.filter(Incidencia.color == color)
        return query.all()

    @staticmethod
    def ranking_resumen(torneo: str | None, categoria: str | None, fecha_hasta: int | None = None):
        return IncidenciaRepository.ranking_resumen(torneo, categoria, fecha_hasta)
