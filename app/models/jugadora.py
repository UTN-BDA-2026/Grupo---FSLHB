"""Modelo Jugadora - Documento MongoDB."""


class Jugadora:
    COLLECTION = 'jugadoras'

    def __init__(self, nombre, apellido, club_id, dni=None,
                 fecha_nacimiento=None, categoria=None, _id=None):
        self._id = _id
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.fecha_nacimiento = fecha_nacimiento
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
            'apellido': self.apellido,
            'dni': self.dni,
            'fecha_nacimiento': self.fecha_nacimiento,
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
            apellido=data.get('apellido'),
            dni=data.get('dni'),
            fecha_nacimiento=data.get('fecha_nacimiento'),
            categoria=data.get('categoria'),
            club_id=data.get('club_id'),
        )

    def __repr__(self):
        return f'<Jugadora {self.apellido}, {self.nombre}>'

    def __eq__(self, other):
        if not isinstance(other, Jugadora):
            return False
        return self._id == other._id