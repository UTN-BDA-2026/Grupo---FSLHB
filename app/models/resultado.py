from app import db

class Resultado(db.Model):
    __tablename__ = "Resultados"

    id = db.Column(db.Integer, primary_key=True)
    club_local = db.Column(db.String(100), nullable=False)
    club_visitante = db.Column(db.String(100), nullable=False)
    goles_local = db.Column(db.Integer, nullable=False)
    goles_visitante = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False)

    