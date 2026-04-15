from app.repositories.nota_partido_repositorio import NotaPartidoRepository

class NotaPartidoService:
    @staticmethod
    def obtener(partido_id: int):
        return NotaPartidoRepository.obtener_por_partido(partido_id)

    @staticmethod
    def guardar(partido_id: int, detalle: str | None):
        return NotaPartidoRepository.upsert(partido_id, detalle)
