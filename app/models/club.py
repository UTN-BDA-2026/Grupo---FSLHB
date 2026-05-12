"""Modelo Club - Documento MongoDB."""
from bson import ObjectId


class Club:
    COLLECTION = 'clubes'

    def __init__(self, nombre, razon_social=None, contacto=None, email=None,
                 cancha_local=None, domicilio=None, telefono=None, web=None,
                 arbitro_id=None, _id=None):
        self._id = _id
        self.nombre = nombre
        self.razon_social = razon_social
        self.contacto = contacto
        self.email = email
        self.cancha_local = cancha_local
        self.domicilio = domicilio
        self.telefono = telefono
        self.web = web
        self.arbitro_id = arbitro_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def to_dict(self):
        d = {
            'nombre': self.nombre,
            'razon_social': self.razon_social,
            'contacto': self.contacto,
            'email': self.email,
            'cancha_local': self.cancha_local,
            'domicilio': self.domicilio,
            'telefono': self.telefono,
            'web': self.web,
            'arbitro_id': self.arbitro_id,
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
            razon_social=data.get('razon_social'),
            contacto=data.get('contacto'),
            email=data.get('email'),
            cancha_local=data.get('cancha_local'),
            domicilio=data.get('domicilio'),
            telefono=data.get('telefono'),
            web=data.get('web'),
            arbitro_id=data.get('arbitro_id'),
        )

    def __repr__(self):
        return f'<Club {self.nombre}>'

    def __eq__(self, other):
        if not isinstance(other, Club):
            return False
        return self._id == other._id