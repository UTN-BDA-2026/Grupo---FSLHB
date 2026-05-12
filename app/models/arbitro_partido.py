"""Modelo ArbitroPartido - Documento MongoDB."""


class ArbitroPartido:
    COLLECTION = 'arbitro_partido'

    def __init__(self, partido_id, arbitro_id, club_id=None, rol=None, _id=None):
        self._id = _id
        self.partido_id = partido_id
        self.club_id = club_id
        self.arbitro_id = arbitro_id
        self.rol = rol  # 'principal', 'asistente', etc.

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
            'arbitro_id': self.arbitro_id,
            'rol': self.rol,
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
            arbitro_id=data.get('arbitro_id'),
            rol=data.get('rol'),
        )

    def __repr__(self):
        return f'<ArbitroPartido partido={self.partido_id} arbitro={self.arbitro_id}>'
