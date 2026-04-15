from app.models import Club
from app.repositories import ClubRepository
from app.services.arbitro_service import ArbitroService

class ClubService:
    @staticmethod
    def crear(club: Club) -> Club:
        return ClubRepository.crear(club)
        
    @staticmethod
    def buscar_por_id(id: int) -> Club:
        return ClubRepository.buscar_por_id(id)
    
    @staticmethod
    def buscar_todos() -> list[Club]:
        return ClubRepository.buscar_todos()
    
    @staticmethod
    def actualizar(club: Club) -> Club:
        club_existente = ClubRepository.buscar_por_id(club.id)
        if not club_existente:
            return None
        club_existente.nombre = club.nombre
        return ClubRepository.actualizar_club(club_existente)
    
    @staticmethod
    def borrar_por_id(id: int) -> Club:
        return ClubRepository.borrar_por_id(id)

    @staticmethod
    def obtener_arbitro(club_id: int):
        club = ClubRepository.buscar_por_id(club_id)
        if not club or not getattr(club, 'arbitro_id', None):
            return None
        return ArbitroService.obtener(club.arbitro_id)

    @staticmethod
    def asignar_arbitro(club_id: int, arbitro_id: int):
        return ClubRepository.asignar_arbitro(club_id, arbitro_id)
