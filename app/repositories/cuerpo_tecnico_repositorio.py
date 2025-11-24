from app.models.cuerpo_tecnico import CuerpoTecnico
from app import db

class CuerpoTecnicoRepositorio:
    @staticmethod
    def crear(data):
        ct = CuerpoTecnico(**data)
        db.session.add(ct)
        db.session.commit()
        return ct

    @staticmethod
    def listar(club_id=None):
        q = CuerpoTecnico.query
        if club_id:
            q = q.filter_by(club_id=club_id)
        # No listar árbitros desde el repositorio (defensa en profundidad)
        q = q.filter(CuerpoTecnico.rol != 'ARB')
        return q.order_by(CuerpoTecnico.id).all()

    @staticmethod
    def eliminar(id):
        ct = CuerpoTecnico.query.get(id)
        if ct:
            db.session.delete(ct)
            db.session.commit()
            return True
        return False

    @staticmethod
    def actualizar(id, data):
        ct = CuerpoTecnico.query.get(id)
        if ct:
            for k, v in data.items():
                setattr(ct, k, v)
            db.session.commit()
            return ct
        return None
