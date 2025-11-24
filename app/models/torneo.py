# app/models/torneo.py
from app import db

class Torneo(db.Model):
    __tablename__ = 'torneos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    max_fechas = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Torneo {self.nombre}>'
