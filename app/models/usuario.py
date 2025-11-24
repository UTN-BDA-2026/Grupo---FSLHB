from app import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Mantener TEXT para evitar truncamientos de hashes largos
    password = db.Column(db.Text, nullable=False)
    # club_id ahora es opcional para permitir usuarios genéricos (operadores)
    club_id = db.Column(db.Integer, db.ForeignKey('Clubes.id'), nullable=True)
    club = db.relationship('Club', backref='usuarios')

    # Permisos básicos: para operadores sin club
    is_operador = db.Column(db.Boolean, nullable=False, default=False)
    puede_cargar_incidencias = db.Column(db.Boolean, nullable=False, default=False)
    puede_precargar_equipos = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Usuario {self.username}>'