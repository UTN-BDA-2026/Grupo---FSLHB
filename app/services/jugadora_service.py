from app.models import Jugadora
from app.repositories.jugadora_repositorio import JugadoraRepository
from app.extensions import mongo

class JugadoraService:
    @staticmethod
    def crear_jugadora(data):
        dni = data.get('dni')
        if dni:
            existente = mongo.db.jugadoras.find_one({'dni': dni})
            if existente:
                return None, 'Ya existe una jugadora con ese DNI'
        jugadora = Jugadora(**data)
        JugadoraRepository.crear(jugadora)
        return jugadora, None
