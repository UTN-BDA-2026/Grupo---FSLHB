from app import db
from app.models.nota_partido import NotaPartido

class NotaPartidoRepository:
    @staticmethod
    def obtener_por_partido(partido_id: int):
        return db.session.query(NotaPartido).filter_by(partido_id=partido_id).first()

    @staticmethod
    def upsert(partido_id: int, detalle: str | None):
        nota = NotaPartidoRepository.obtener_por_partido(partido_id)
        if nota is None:
            nota = NotaPartido(partido_id=partido_id, detalle=detalle)
            db.session.add(nota)
        else:
            nota.detalle = detalle
        db.session.commit()
        return nota
