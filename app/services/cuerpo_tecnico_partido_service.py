from app.repositories.cuerpo_tecnico_partido_repositorio import CuerpoTecnicoPartidoRepositorio
from app.models.cuerpo_tecnico_partido import CuerpoTecnicoPartido


class CuerpoTecnicoPartidoService:
    @staticmethod
    def guardar(partido_id: int, club_id: int, rol: str, cuerpo_tecnico_id: int) -> CuerpoTecnicoPartido:
        rol_norm = (rol or '').strip().lower()
        if rol_norm not in ('director_tecnico', 'preparador_fisico'):
            raise ValueError('rol invalido')
        return CuerpoTecnicoPartidoRepositorio.upsert(partido_id, club_id, rol_norm, cuerpo_tecnico_id)

    @staticmethod
    def listar_por_partido(partido_id: int):
        return CuerpoTecnicoPartidoRepositorio.listar_por_partido(partido_id)
