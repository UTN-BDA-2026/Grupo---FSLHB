from app.repositories.cuerpo_tecnico_repositorio import CuerpoTecnicoRepositorio

ALLOWED_ROLES = { 'DT', 'PF' }

class CuerpoTecnicoService:
    @staticmethod
    def crear(data):
        rol = (data or {}).get('rol')
        if rol not in ALLOWED_ROLES:
            raise ValueError('Rol no permitido para Cuerpo Técnico')
        return CuerpoTecnicoRepositorio.crear(data)

    @staticmethod
    def listar(club_id=None):
        return CuerpoTecnicoRepositorio.listar(club_id)

    @staticmethod
    def eliminar(id):
        return CuerpoTecnicoRepositorio.eliminar(id)

    @staticmethod
    def actualizar(id, data):
        if data and 'rol' in data:
            rol = data.get('rol')
            if rol not in ALLOWED_ROLES:
                raise ValueError('Rol no permitido para Cuerpo Técnico')
        return CuerpoTecnicoRepositorio.actualizar(id, data)
