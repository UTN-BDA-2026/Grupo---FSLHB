from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class Club(db.Model):
    __tablename__ = "Clubes"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    razon_social = db.Column(db.String(150), nullable=True)
    contacto = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    cancha_local = db.Column(db.String(100), nullable=True)
    domicilio = db.Column(db.String(150), nullable=True)
    telefono = db.Column(db.String(50), nullable=True)
    web = db.Column(db.String(150), nullable=True)
    arbitro_id = db.Column(db.Integer, nullable=True)  # Si tienes árbitros como tabla aparte, puedes hacer ForeignKey