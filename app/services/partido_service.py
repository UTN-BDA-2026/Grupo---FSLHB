from app.models.partido import Partido
from app.repositories.partido_repositorio import PartidoRepository

class PartidoService:
    @staticmethod
    def crear_partido(data: dict):
        partido = Partido(**data)
        return PartidoRepository.crear(partido)

    @staticmethod
    def listar_partidos(filtros: dict):
        return PartidoRepository.buscar(filtros)

    @staticmethod
    def obtener_por_id(id: int):
        return PartidoRepository.buscar_por_id(id)

    @staticmethod
    def marcar_resultado(id: int, goles_local: int, goles_visitante: int):
        partido = PartidoRepository.buscar_por_id(id)
        if not partido:
            return None
        partido.goles_local = goles_local
        partido.goles_visitante = goles_visitante
        partido.estado = 'jugado'
        return PartidoRepository.actualizar(partido)

    @staticmethod
    def abrir_partido(id: int):
        partido = PartidoRepository.buscar_por_id(id)
        if not partido:
            return None
        partido.estado = 'en_juego'
        return PartidoRepository.actualizar(partido)

    @staticmethod
    def cerrar_partido(id: int):
        partido = PartidoRepository.buscar_por_id(id)
        if not partido:
            return None
        # Por ahora consideramos que al cerrar queda como 'jugado'.
        partido.estado = 'jugado'
        return PartidoRepository.actualizar(partido)
