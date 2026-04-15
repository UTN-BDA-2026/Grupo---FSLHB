from app.models import Jugadora
from app.repositories.jugadora_repositorio import JugadoraRepository

class JugadoraService:
    @staticmethod
    def crear_jugadora(data):
        dni = data.get('dni')
        if dni:
            existente = Jugadora.query.filter_by(dni=dni).first()
            if existente:
                return None, 'Ya existe una jugadora con ese DNI'
        jugadora = Jugadora(**data)
        JugadoraRepository.crear(jugadora)
        return jugadora, None
