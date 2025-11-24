from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class Equipo(db.Model):
    __tablename__ = "Equipos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=True)
    club_id = db.Column(db.Integer, db.ForeignKey('Clubes.id'), nullable=False)
    club = db.relationship('Club', backref='equipos')
