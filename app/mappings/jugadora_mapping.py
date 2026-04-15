from marshmallow import Schema, fields, post_load, validate
from app.models import Jugadora

class JugadoraSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    apellido = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    dni = fields.Str(required=False, allow_none=True)
    fecha_nacimiento = fields.Str(required=False, allow_none=True)
    categoria = fields.Str(required=False, allow_none=True)
    club_id = fields.Int(required=True)

    @post_load
    def crear_jugadora(self, data, **kwargs):
        return Jugadora(**data)
