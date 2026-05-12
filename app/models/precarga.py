"""Modelo PrecargaJugadora - Documento MongoDB."""
from datetime import datetime


class PrecargaJugadora:
    COLLECTION = 'precarga_jugadoras'

    def __init__(self, partido_id, club_id, jugadora_id, created_at=None, _id=None):
        self._id = _id
        self.partido_id = partido_id
        self.club_id = club_id
        self.jugadora_id = jugadora_id
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
            created_at=data.get('created_at'),
        )
