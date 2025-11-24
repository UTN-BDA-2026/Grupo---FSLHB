from dataclasses import dataclass
from datetime import datetime
from app import db

@dataclass(init=False, repr=True, eq=True)
class Incidencia(db.Model):
    __tablename__ = "Incidencias"

    id = db.Column(db.Integer, primary_key=True)
    partido_id = db.Column(db.Integer, db.ForeignKey('Partidos.id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('Clubes.id'), nullable=False)
    jugadora_id = db.Column(db.Integer, db.ForeignKey('Jugadoras.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'gol' | 'tarjeta'
    color = db.Column(db.String(20), nullable=True)  # 'verde' | 'amarilla' | 'roja' (solo si tipo='tarjeta')
    minuto = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
