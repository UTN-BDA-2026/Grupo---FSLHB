from app import db
from app.models.cuerpo_tecnico_partido import CuerpoTecnicoPartido
from sqlalchemy.exc import ProgrammingError, OperationalError


class CuerpoTecnicoPartidoRepositorio:
    @staticmethod
    def upsert(partido_id: int, club_id: int, rol: str, cuerpo_tecnico_id: int):
        row = CuerpoTecnicoPartido.query.filter_by(partido_id=partido_id, club_id=club_id, rol=rol).first()
        if row:
            row.cuerpo_tecnico_id = cuerpo_tecnico_id
        else:
            row = CuerpoTecnicoPartido(
                partido_id=partido_id,
                club_id=club_id,
                rol=rol,
                cuerpo_tecnico_id=cuerpo_tecnico_id,
            )
            db.session.add(row)
        db.session.commit()
        return row

    @staticmethod
    def listar_por_partido(partido_id: int):
        try:
            return CuerpoTecnicoPartido.query.filter_by(partido_id=partido_id).all()
        except (ProgrammingError, OperationalError):
            # Tabla aún no creada (falta migración): devolver vacío para evitar 500
            db.session.rollback()
            return []
