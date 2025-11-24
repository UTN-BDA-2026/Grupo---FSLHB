from marshmallow import Schema, fields, post_load
from app.models import Resultado

class ResultadoSchema(Schema):
    id = fields.Int(dump_only=True)
    club_local = fields.Str(required=True)
    club_visitante = fields.Str(required=True)
    goles_local = fields.Int(required=True)
    goles_visitante = fields.Int(required=True)
    fecha = fields.Date(required=True)

    @post_load
    def crear_resultado(self, datos, **kwargs):
        return Resultado(**datos)
