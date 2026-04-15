from app.repositories.precarga_repositorio import PrecargaRepository

class PrecargaService:
    @staticmethod
    def obtener(partido_id: int, club_id: int):
        return PrecargaRepository.listar(partido_id, club_id)

    @staticmethod
    def guardar(partido_id: int, club_id: int, jugadora_ids: list[int]):
        return PrecargaRepository.guardar_lista(partido_id, club_id, jugadora_ids)

    @staticmethod
    def obtener_alineaciones(partido_id: int):
        return PrecargaRepository.listar_con_detalle_por_partido(partido_id)
