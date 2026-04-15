from app import db
from app.models.precarga import PrecargaJugadora
from app.models.jugadora import Jugadora

class PrecargaRepository:
    @staticmethod
    def listar(partido_id: int, club_id: int):
        return db.session.query(PrecargaJugadora).filter_by(partido_id=partido_id, club_id=club_id).all()

    @staticmethod
    def guardar_lista(partido_id: int, club_id: int, jugadora_ids: list[int]):
        # eliminar actuales y crear nuevas (sencillo y robusto)
        db.session.query(PrecargaJugadora).filter_by(partido_id=partido_id, club_id=club_id).delete()
        for jid in jugadora_ids:
            db.session.add(PrecargaJugadora(partido_id=partido_id, club_id=club_id, jugadora_id=jid))
        db.session.commit()
        return True

    @staticmethod
    def listar_con_detalle_por_partido(partido_id: int):
        # Devuelve dict: { club_id: [ {id, nombre, apellido, dni, categoria}, ... ] }
        rows = (
            db.session.query(PrecargaJugadora.club_id,
                             Jugadora.id,
                             Jugadora.nombre,
                             Jugadora.apellido,
                             Jugadora.dni,
                             Jugadora.categoria)
            .join(Jugadora, Jugadora.id == PrecargaJugadora.jugadora_id)
            .filter(PrecargaJugadora.partido_id == partido_id)
            .order_by(PrecargaJugadora.club_id, Jugadora.apellido, Jugadora.nombre)
            .all()
        )
        result: dict[int, list[dict]] = {}
        for club_id, jid, nombre, apellido, dni, categoria in rows:
            result.setdefault(club_id, []).append({
                'id': jid,
                'nombre': nombre,
                'apellido': apellido,
                'dni': dni,
                'categoria': categoria,
            })
        return result
