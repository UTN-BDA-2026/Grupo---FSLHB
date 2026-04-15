from app import db
from app.models import Club

class ClubRepository:
    @staticmethod
    def crear(club):
        db.session.add(club)
        db.session.commit()
    
    @staticmethod
    def buscar_por_id(id:int):
        return db.session.query(Club).filter_by(id=id).first()

    @staticmethod
    def buscar_todos():
        return db.session.query(Club).all()

    @staticmethod
    def actualizar_club(club):
        club_existente = db.session.merge(club)
        if not club_existente:
            return None
        db.session.commit()
        return club_existente

    @staticmethod
    def asignar_arbitro(club_id: int, arbitro_id: int):
        club = db.session.query(Club).filter_by(id=club_id).first()
        if not club:
            return None
        club.arbitro_id = arbitro_id
        db.session.commit()
        return club
    
    @staticmethod
    def borrar_por_id(id:int):
        club = db.session.query(Club).filter_by(id=id).first()
        if not club:
            return None
        db.session.delete(club)
        db.session.commit()
        return club
