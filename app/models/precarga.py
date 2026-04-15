from dataclasses import dataclass
from datetime import datetime
from app import db

@dataclass(init=False, repr=True, eq=True)
class PrecargaJugadora(db.Model):
    __tablename__ = "PrecargaJugadoras"

    id = db.Column(db.Integer, primary_key=True)
    partido_id = db.Column(db.Integer, db.ForeignKey('Partidos.id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('Clubes.id'), nullable=False)
    jugadora_id = db.Column(db.Integer, db.ForeignKey('Jugadoras.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('partido_id', 'club_id', 'jugadora_id', name='uq_precarga_partido_club_jugadora'),
    )
