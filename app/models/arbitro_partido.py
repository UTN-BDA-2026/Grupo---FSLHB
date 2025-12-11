from app import db


class ArbitroPartido(db.Model):
    __tablename__ = 'arbitro_partido'

    id = db.Column(db.Integer, primary_key=True)
    partido_id = db.Column(db.Integer, db.ForeignKey('Partidos.id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('Clubes.id'), nullable=True)  # árbitro asignado para un equipo del partido
    arbitro_id = db.Column(db.Integer, db.ForeignKey('arbitros.id'), nullable=False)
    rol = db.Column(db.String(32), nullable=True)  # opcional: 'principal', 'asistente', etc.

    __table_args__ = (
        db.UniqueConstraint('partido_id', 'club_id', name='uq_arbitro_partido_equipo'),
    )

    arbitro = db.relationship('Arbitro', backref='designaciones')
