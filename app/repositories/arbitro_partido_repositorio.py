from app import db
from app.models.arbitro_partido import ArbitroPartido
from app.models.arbitro import Arbitro


class ArbitroPartidoRepositorio:
    @staticmethod
    def listar_por_partido(partido_id: int):
        return (
            db.session.query(ArbitroPartido, Arbitro)
            .join(Arbitro, ArbitroPartido.arbitro_id == Arbitro.id)
            .filter(ArbitroPartido.partido_id == partido_id)
            .order_by(Arbitro.apellido, Arbitro.nombre)
            .all()
        )

    @staticmethod
    def set_lista(partido_id: int, arbitro_ids: list[int]):
        # Normalizar a set de enteros
        target = set(int(x) for x in (arbitro_ids or []) if x)
        existentes = ArbitroPartido.query.filter_by(partido_id=partido_id).all()
        actuales = set(r.arbitro_id for r in existentes)

        # Eliminar los que sobran
        for row in existentes:
            if row.arbitro_id not in target:
                db.session.delete(row)

        # Agregar faltantes
        for arb_id in target - actuales:
            db.session.add(ArbitroPartido(partido_id=partido_id, arbitro_id=int(arb_id)))

        db.session.commit()

        # Devolver lista actualizada
        return ArbitroPartidoRepositorio.listar_por_partido(partido_id)
