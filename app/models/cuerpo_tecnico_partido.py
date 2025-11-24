from dataclasses import dataclass
from app import db


@dataclass(init=False, repr=True, eq=True)
class CuerpoTecnicoPartido(db.Model):
    __tablename__ = 'cuerpo_tecnico_partido'

    id = db.Column(db.Integer, primary_key=True)
    partido_id = db.Column(db.Integer, db.ForeignKey('Partidos.id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('Clubes.id'), nullable=False)
    # rol esperado: 'director_tecnico' | 'preparador_fisico'
    rol = db.Column(db.String(32), nullable=False)
    cuerpo_tecnico_id = db.Column(db.Integer, db.ForeignKey('cuerpo_tecnico.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('partido_id', 'club_id', 'rol', name='uq_ct_partido_club_rol'),
    )
