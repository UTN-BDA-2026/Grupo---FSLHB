"""Modelo Jugadora - MariaDB (SQLAlchemy)."""

from app.extensions import db


class Jugadora(db.Model):
    __tablename__ = 'jugadoras'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(32), unique=True, nullable=True)
    # Se mantiene como string (YYYY-MM-DD) para compatibilidad con frontend actual.
    fecha_nacimiento = db.Column(db.String(32), nullable=True)
    categoria = db.Column(db.String(64), nullable=True)
    # En Mongo, los clubes usan ObjectId; acá se guarda como string hex (24 chars).
    club_id = db.Column(db.String(64), nullable=False, index=True)

    def __repr__(self):
        return f'<Jugadora {self.apellido}, {self.nombre}>'