from app.extensions import db
from app.models.jugadora import Jugadora


class JugadoraRepository:
    @staticmethod
    def crear(jugadora):
        db.session.add(jugadora)
        db.session.commit()
        return jugadora

    @staticmethod
    def buscar_por_id(id):
        try:
            jid = int(str(id).strip())
        except Exception:
            return None
        return db.session.get(Jugadora, jid)

    @staticmethod
    def buscar_todas():
        return Jugadora.query.all()

    @staticmethod
    def buscar_por_club(club_id):
        if club_id is None:
            return []
        cid = str(club_id).strip()
        if not cid or cid.lower() in ('null', 'undefined', 'none'):
            return []
        return Jugadora.query.filter_by(club_id=cid).all()

    @staticmethod
    def buscar_por_dni(dni: str):
        if not dni:
            return None
        return Jugadora.query.filter_by(dni=str(dni).strip()).first()

    @staticmethod
    def actualizar_jugadora(jugadora):
        db.session.add(jugadora)
        db.session.commit()
        return jugadora

    @staticmethod
    def borrar_por_id(id):
        jugadora = JugadoraRepository.buscar_por_id(id)
        if not jugadora:
            return None
        db.session.delete(jugadora)
        db.session.commit()
        return jugadora
