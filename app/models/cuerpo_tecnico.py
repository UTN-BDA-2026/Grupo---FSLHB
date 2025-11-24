from app import db

class CuerpoTecnico(db.Model):
    __tablename__ = 'cuerpo_tecnico'
    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('Clubes.id'), nullable=False)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    dni = db.Column(db.String(20), nullable=False)
    rol = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    club = db.relationship('Club', backref='cuerpo_tecnico')
