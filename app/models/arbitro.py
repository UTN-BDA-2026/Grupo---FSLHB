"""Modelo Arbitro - Documento MongoDB."""
from datetime import datetime


class Arbitro:
    COLLECTION = 'arbitros'

    def __init__(self, nombre, apellido, dni, created_at=None, _id=None):
        self._id = _id
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.created_at = created_at or datetime.utcnow()

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
            nombre=data.get('nombre'),
            apellido=data.get('apellido'),
            dni=data.get('dni'),
            created_at=data.get('created_at'),
        )

    def __repr__(self):
        return f"<Arbitro {self.apellido}, {self.nombre} ({self.dni})>"
