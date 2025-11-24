from app import db


class Arbitro(db.Model):
    __tablename__ = 'arbitros'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    dni = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self) -> str:
        return f"<Arbitro {self.apellido}, {self.nombre} ({self.dni})>"
