"""Modelo Usuario - Documento MongoDB."""
from flask_login import UserMixin


class Usuario(UserMixin):
    COLLECTION = 'usuarios'

    def __init__(self, username, password, club_id=None,
                 is_operador=False, puede_cargar_incidencias=False,
                 puede_precargar_equipos=False, is_admin=False, _id=None):
        self._id = _id
        self.username = username
        self.password = password
        self.club_id = club_id
        self.is_operador = is_operador
        self.puede_cargar_incidencias = puede_cargar_incidencias
        self.puede_precargar_equipos = puede_precargar_equipos
        self.is_admin = is_admin

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def get_id(self):
        """Override UserMixin para usar _id de MongoDB (string)."""
        return str(self._id)

    def to_dict(self):
        d = {
            'username': self.username,
            'password': self.password,
            'club_id': self.club_id,
            'is_operador': self.is_operador,
            'puede_cargar_incidencias': self.puede_cargar_incidencias,
            'puede_precargar_equipos': self.puede_precargar_equipos,
            'is_admin': self.is_admin,
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
            username=data.get('username'),
            password=data.get('password'),
            club_id=data.get('club_id'),
            is_operador=data.get('is_operador', False),
            puede_cargar_incidencias=data.get('puede_cargar_incidencias', False),
            puede_precargar_equipos=data.get('puede_precargar_equipos', False),
            is_admin=data.get('is_admin', False),
        )

    def __repr__(self):
        return f'<Usuario {self.username}>'