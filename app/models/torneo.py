"""Modelo Torneo - Documento MongoDB."""


class Torneo:
    COLLECTION = 'torneos'

    def __init__(self, nombre, max_fechas, _id=None):
        self._id = _id
        self.nombre = nombre
        self.max_fechas = max_fechas

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def to_dict(self):
        d = {
            'nombre': self.nombre,
            'max_fechas': self.max_fechas,
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
            nombre=data.get('nombre'),
            max_fechas=data.get('max_fechas'),
        )

    def __repr__(self):
        return f'<Torneo {self.nombre}>'
