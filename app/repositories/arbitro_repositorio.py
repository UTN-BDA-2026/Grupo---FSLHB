from app import db
from app.models.arbitro import Arbitro


class ArbitroRepositorio:
    @staticmethod
    def crear(data: dict) -> Arbitro:
        arb = Arbitro(**data)
        db.session.add(arb)
        db.session.commit()
        return arb

    @staticmethod
    def obtener(id: int) -> Arbitro | None:
        return Arbitro.query.get(id)

    @staticmethod
    def listar() -> list[Arbitro]:
        return Arbitro.query.order_by(Arbitro.apellido, Arbitro.nombre).all()

    @staticmethod
    def eliminar(id: int) -> bool:
        arb = Arbitro.query.get(id)
        if not arb:
            return False
        db.session.delete(arb)
        db.session.commit()
        return True

    @staticmethod
    def actualizar(id: int, nombre: str | None = None, apellido: str | None = None) -> Arbitro | None:
        arb = Arbitro.query.get(id)
        if not arb:
            return None
        if nombre is not None:
            arb.nombre = nombre
        if apellido is not None:
            arb.apellido = apellido
        db.session.commit()
        return arb
