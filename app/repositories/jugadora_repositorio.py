from app import db
from app.models import Jugadora

class JugadoraRepository:
    @staticmethod
    def crear(jugadora):
        db.session.add(jugadora)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id:int):
        return db.session.query(Jugadora).filter_by(id=id).first()

    @staticmethod
    def buscar_todas():
        return db.session.query(Jugadora).all()

    @staticmethod
    def buscar_por_club(club_id):
        return db.session.query(Jugadora).filter_by(club_id=club_id).all()

    @staticmethod
    def actualizar_jugadora(jugadora):
        jugadora_existente = db.session.merge(jugadora)
        if not jugadora_existente:
            return None
        db.session.commit()
        return jugadora_existente

    @staticmethod
    def borrar_por_id(id:int):
        jugadora = db.session.query(Jugadora).filter_by(id=id).first()
        if not jugadora:
            return None
        db.session.delete(jugadora)
        db.session.commit()
        return jugadora
