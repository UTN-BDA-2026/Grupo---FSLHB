"""Modelo Equipo - Documento MongoDB."""


class Equipo:
    COLLECTION = 'equipos'

    def __init__(self, nombre, club_id, categoria=None, _id=None):
        self._id = _id
        self.nombre = nombre
        self.categoria = categoria
        self.club_id = club_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def to_dict(self):
        d = {
            'nombre': self.nombre,
            'categoria': self.categoria,
            'club_id': self.club_id,
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
            categoria=data.get('categoria'),
            club_id=data.get('club_id'),
        )

    def __repr__(self):
        return f'<Equipo {self.nombre}>'

    def __eq__(self, other):
        if not isinstance(other, Equipo):
            return False
        return self._id == other._id
