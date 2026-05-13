from app.models import Jugadora
from app.repositories.jugadora_repositorio import JugadoraRepository

class JugadoraService:
    @staticmethod
    def crear_jugadora(data):
        dni = data.get('dni')
        if dni:
            existente = JugadoraRepository.buscar_por_dni(dni)
            if existente:
                return None, 'Ya existe una jugadora con ese DNI'
        jugadora = Jugadora(**data)
        JugadoraRepository.crear(jugadora)
        return jugadora, None
