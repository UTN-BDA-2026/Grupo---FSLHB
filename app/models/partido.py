"""Modelo Partido - Documento MongoDB."""
from datetime import datetime


class Partido:
    COLLECTION = 'partidos'

    def __init__(self, torneo, categoria, club_local_id, club_visitante_id,
                 fecha_numero=None, bloque=None, fecha_hora=None, cancha=None,
                 equipo_local_id=None, equipo_visitante_id=None,
                 estado='programado', goles_local=None, goles_visitante=None,
                 _id=None):
        self._id = _id
        self.torneo = torneo
        self.categoria = categoria
        self.fecha_numero = fecha_numero
        self.bloque = bloque
        self.fecha_hora = fecha_hora
        self.cancha = cancha
        self.club_local_id = club_local_id
        self.club_visitante_id = club_visitante_id
        self.equipo_local_id = equipo_local_id
        self.equipo_visitante_id = equipo_visitante_id
        self.estado = estado
        self.goles_local = goles_local
        self.goles_visitante = goles_visitante

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def to_dict(self):
        d = {
            'torneo': self.torneo,
            'categoria': self.categoria,
            'fecha_numero': self.fecha_numero,
            'bloque': self.bloque,
            'fecha_hora': self.fecha_hora,
            'cancha': self.cancha,
            'club_local_id': self.club_local_id,
            'club_visitante_id': self.club_visitante_id,
            'equipo_local_id': self.equipo_local_id,
            'equipo_visitante_id': self.equipo_visitante_id,
            'estado': self.estado,
            'goles_local': self.goles_local,
            'goles_visitante': self.goles_visitante,
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
            torneo=data.get('torneo'),
            categoria=data.get('categoria'),
            fecha_numero=data.get('fecha_numero'),
            bloque=data.get('bloque'),
            fecha_hora=data.get('fecha_hora'),
            cancha=data.get('cancha'),
            club_local_id=data.get('club_local_id'),
            club_visitante_id=data.get('club_visitante_id'),
            equipo_local_id=data.get('equipo_local_id'),
            equipo_visitante_id=data.get('equipo_visitante_id'),
            estado=data.get('estado', 'programado'),
            goles_local=data.get('goles_local'),
            goles_visitante=data.get('goles_visitante'),
        )

    def __repr__(self):
        return f'<Partido {self._id} {self.torneo} {self.categoria}>'

    def __eq__(self, other):
        if not isinstance(other, Partido):
            return False
        return self._id == other._id
