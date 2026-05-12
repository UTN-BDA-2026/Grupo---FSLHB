"""Modelo Noticia - Documento MongoDB."""


class Noticia:
    COLLECTION = 'noticias'

    def __init__(self, titulo, contenido, resumen=None, imagen=None,
                 fecha=None, _id=None):
        self._id = _id
        self.titulo = titulo
        self.resumen = resumen
        self.contenido = contenido
        self.imagen = imagen
        self.fecha = fecha

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def to_dict(self):
        d = {
            'titulo': self.titulo,
            'resumen': self.resumen,
            'contenido': self.contenido,
            'imagen': self.imagen,
            'fecha': self.fecha,
        }
        if self._id is not None:
            d['_id'] = self._id
        return d

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        return cls(
            _id=data.get('_id'),
            titulo=data.get('titulo'),
            resumen=data.get('resumen'),
            contenido=data.get('contenido'),
            imagen=data.get('imagen'),
            fecha=data.get('fecha'),
        )

    def __repr__(self):
        return f'<Noticia {self.titulo}>'
