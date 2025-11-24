from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class Partido(db.Model):
    __tablename__ = "Partidos"

    id = db.Column(db.Integer, primary_key=True)
    torneo = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    fecha_numero = db.Column(db.Integer, nullable=True)
    bloque = db.Column(db.String(5), nullable=True)
    fecha_hora = db.Column(db.DateTime, nullable=True)
    cancha = db.Column(db.String(100), nullable=True)

    club_local_id = db.Column(db.Integer, db.ForeignKey('Clubes.id'), nullable=False)
    club_visitante_id = db.Column(db.Integer, db.ForeignKey('Clubes.id'), nullable=False)
    # Nuevos campos opcionales para identificar el equipo específico (A, B, etc.)
    equipo_local_id = db.Column(db.Integer, db.ForeignKey('Equipos.id'), nullable=True)
    equipo_visitante_id = db.Column(db.Integer, db.ForeignKey('Equipos.id'), nullable=True)

    estado = db.Column(db.String(20), nullable=False, default='programado')
    goles_local = db.Column(db.Integer, nullable=True)
    goles_visitante = db.Column(db.Integer, nullable=True)

    # Relaciones a Club
    club_local = db.relationship('Club', foreign_keys=[club_local_id])
    club_visitante = db.relationship('Club', foreign_keys=[club_visitante_id])
    # Relaciones a Equipo (opcional)
    equipo_local = db.relationship('Equipo', foreign_keys=[equipo_local_id])
    equipo_visitante = db.relationship('Equipo', foreign_keys=[equipo_visitante_id])
