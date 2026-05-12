"""Modelo CuerpoTecnicoPartido - Documento MongoDB."""


class CuerpoTecnicoPartido:
    COLLECTION = 'cuerpo_tecnico_partido'

    def __init__(self, partido_id, club_id, rol, cuerpo_tecnico_id, _id=None):
        self._id = _id
        self.partido_id = partido_id
        self.club_id = club_id
        self.rol = rol  # 'director_tecnico' | 'preparador_fisico'
        self.cuerpo_tecnico_id = cuerpo_tecnico_id

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
            'rol': self.rol,
            'cuerpo_tecnico_id': self.cuerpo_tecnico_id,
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
            rol=data.get('rol'),
            cuerpo_tecnico_id=data.get('cuerpo_tecnico_id'),
        )

    def __repr__(self):
        return f'<CuerpoTecnicoPartido partido={self.partido_id} rol={self.rol}>'
