from app.repositories.arbitro_partido_repositorio import ArbitroPartidoRepositorio
from app.services.arbitro_service import ArbitroService


class ArbitroPartidoService:
    @staticmethod
    def listar(partido_id: int):
        filas = ArbitroPartidoRepositorio.listar_por_partido(partido_id)
        return [
            {
                'id': ap.id,
                'partido_id': ap.partido_id,
                'arbitro_id': a.id,
                'rol': ap.rol,
                'arbitro': {
                    'id': a.id,
                    'nombre': a.nombre,
                    'apellido': a.apellido,
                    'dni': a.dni,
                }
            } for (ap, a) in filas
        ]

    @staticmethod
    def set_lista(partido_id: int, arbitro_ids: list[int]):
        if arbitro_ids is None:
            arbitro_ids = []
        # opcional: limitar a máximo 2 árbitros
        if len(arbitro_ids) > 2:
            raise ValueError('Máximo 2 árbitros por partido')
        # validar que existan
        for aid in arbitro_ids:
            if not ArbitroService.obtener(int(aid)):
                raise ValueError(f'Árbitro {aid} no existe')
        return ArbitroPartidoRepositorio.set_lista(partido_id, [int(x) for x in arbitro_ids])
