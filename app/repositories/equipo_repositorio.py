from app import db
from app.models.equipo import Equipo

class EquipoRepository:
    @staticmethod
    def crear(equipo):
        db.session.add(equipo)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(Equipo).filter_by(id=id).first()

    @staticmethod
    def buscar_todos():
        return db.session.query(Equipo).all()

    @staticmethod
    def buscar_por_club(club_id):
        return db.session.query(Equipo).filter_by(club_id=club_id).all()

    @staticmethod
    def buscar_por_categoria(categoria: str):
        if not categoria:
            return db.session.query(Equipo).all()
        return db.session.query(Equipo).filter(Equipo.categoria.ilike(f"%{categoria}%")).all()

    @staticmethod
    def actualizar_equipo(equipo):
        equipo_existente = db.session.merge(equipo)
        if not equipo_existente:
            return None
        db.session.commit()
        return equipo_existente

    @staticmethod
    def borrar_por_id(id: int):
        equipo = db.session.query(Equipo).filter_by(id=id).first()
        if not equipo:
            return None
        db.session.delete(equipo)
        db.session.commit()
        return equipo
