from app import db

class Noticia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    resumen = db.Column(db.Text, nullable=True)
    contenido = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(255), nullable=True)
    fecha = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'resumen': self.resumen,
            'contenido': self.contenido,
            'imagen': self.imagen,
            'fecha': self.fecha
        }
