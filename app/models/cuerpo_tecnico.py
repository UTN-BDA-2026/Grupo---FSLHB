"""Modelo CuerpoTecnico - Documento MongoDB."""
from datetime import datetime


class CuerpoTecnico:
    COLLECTION = 'cuerpo_tecnico'

    def __init__(self, club_id, nombre, apellido, dni, rol,
                 created_at=None, _id=None):
        self._id = _id
        self.club_id = club_id
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.rol = rol
        self.created_at = created_at or datetime.utcnow()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def to_dict(self):
        d = {
            'club_id': self.club_id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'dni': self.dni,
            'rol': self.rol,
            'created_at': self.created_at,
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
            club_id=data.get('club_id'),
            nombre=data.get('nombre'),
            apellido=data.get('apellido'),
            dni=data.get('dni'),
            rol=data.get('rol'),
            created_at=data.get('created_at'),
        )

    def __repr__(self):
        return f'<CuerpoTecnico {self.apellido}, {self.nombre} ({self.rol})>'
