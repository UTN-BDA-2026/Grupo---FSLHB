"""Modelo Resultado - Documento MongoDB."""


class Resultado:
    COLLECTION = 'resultados'

    def __init__(self, club_local, club_visitante, goles_local, goles_visitante,
                 fecha, _id=None):
        self._id = _id
        self.club_local = club_local
        self.club_visitante = club_visitante
        self.goles_local = goles_local
        self.goles_visitante = goles_visitante
        self.fecha = fecha

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def to_dict(self):
        d = {
            'club_local': self.club_local,
            'club_visitante': self.club_visitante,
            'goles_local': self.goles_local,
            'goles_visitante': self.goles_visitante,
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
            club_local=data.get('club_local'),
            club_visitante=data.get('club_visitante'),
            goles_local=data.get('goles_local'),
            goles_visitante=data.get('goles_visitante'),
            fecha=data.get('fecha'),
        )