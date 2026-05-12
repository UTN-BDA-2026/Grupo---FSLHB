"""Modelo NotaPartido - Documento MongoDB."""


class NotaPartido:
    COLLECTION = 'notas_partido'

    def __init__(self, partido_id, detalle=None, _id=None):
        self._id = _id
        self.partido_id = partido_id
        self.detalle = detalle

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def to_dict(self):
        d = {
            'partido_id': self.partido_id,
            'detalle': self.detalle,
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
            detalle=data.get('detalle'),
        )

    def __repr__(self):
        return f'<NotaPartido partido={self.partido_id}>'
