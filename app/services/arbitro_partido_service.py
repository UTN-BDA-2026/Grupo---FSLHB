from app.repositories.arbitro_partido_repositorio import ArbitroPartidoRepositorio
from app.services.arbitro_service import ArbitroService


class ArbitroPartidoService:
    @staticmethod
    def listar(partido_id: int):
        filas = ArbitroPartidoRepositorio.listar_por_partido(partido_id)
        # Devuelve lista completa y además mapea por club_id si está presente
        asignados = []
        for (ap, a) in filas:
            asignados.append({
                'id': ap.id,
                'partido_id': ap.partido_id,
                'club_id': getattr(ap, 'club_id', None),
                'arbitro_id': a.id,
                'rol': ap.rol,
                'arbitro': {
                    'id': a.id,
                    'nombre': a.nombre,
                    'apellido': a.apellido,
                    'dni': a.dni,
                }
            })
        return asignados

    @staticmethod
    def set_por_equipo(partido_id: int, club_id: int, arbitro_id: int | None):
        if arbitro_id is not None:
            if not ArbitroService.obtener(int(arbitro_id)):
                raise ValueError(f'Árbitro {arbitro_id} no existe')
        return ArbitroPartidoRepositorio.set_por_equipo(partido_id, int(club_id), (int(arbitro_id) if arbitro_id is not None else None))
