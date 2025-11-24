from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class Jugadora(db.Model):
    __tablename__="Jugadoras"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), nullable=True)
    fecha_nacimiento = db.Column(db.String(20), nullable=True)
    categoria = db.Column(db.String(50), nullable=True)
    club_id = db.Column(db.Integer, db.ForeignKey('Clubes.id'), nullable=False)
    club = db.relationship('Club', backref='jugadoras')
    