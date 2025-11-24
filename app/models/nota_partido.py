from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class NotaPartido(db.Model):
    __tablename__ = "NotasPartido"

    id = db.Column(db.Integer, primary_key=True)
    partido_id = db.Column(db.Integer, db.ForeignKey('Partidos.id'), nullable=False, unique=True)
    detalle = db.Column(db.Text, nullable=True)
