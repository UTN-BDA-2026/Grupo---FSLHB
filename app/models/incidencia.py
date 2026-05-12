"""Modelo Incidencia - Documento MongoDB."""
from datetime import datetime


class Incidencia:
    COLLECTION = 'incidencias'

    def __init__(self, partido_id, club_id, jugadora_id, tipo,
                 color=None, minuto=None, created_at=None, _id=None):
        self._id = _id
        self.partido_id = partido_id
        self.club_id = club_id
        self.jugadora_id = jugadora_id
        self.tipo = tipo  # 'gol' | 'tarjeta'
        self.color = color  # 'verde' | 'amarilla' | 'roja' (solo si tipo='tarjeta')
        self.minuto = minuto
        self.created_at = created_at or datetime.utcnow()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def to_dict(self):
        d = {
            'partido_id': self.partido_id,
            'club_id': self.club_id,
            'jugadora_id': self.jugadora_id,
            'tipo': self.tipo,
            'color': self.color,
            'minuto': self.minuto,
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
            partido_id=data.get('partido_id'),
            club_id=data.get('club_id'),
            jugadora_id=data.get('jugadora_id'),
            tipo=data.get('tipo'),
            color=data.get('color'),
            minuto=data.get('minuto'),
            created_at=data.get('created_at'),
        )

    def __repr__(self):
        return f'<Incidencia {self.tipo} partido={self.partido_id}>'

    def __eq__(self, other):
        if not isinstance(other, Incidencia):
            return False
        return self._id == other._id
