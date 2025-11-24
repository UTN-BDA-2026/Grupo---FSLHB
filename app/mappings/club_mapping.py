from marshmallow import Schema, fields, post_load, validate
from app.models import Club


class ClubMapping(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    razon_social = fields.Str(allow_none=True)
    contacto = fields.Str(allow_none=True)
    email = fields.Str(allow_none=True)
    cancha_local = fields.Str(allow_none=True)
    domicilio = fields.Str(allow_none=True)
    telefono = fields.Str(allow_none=True)
    web = fields.Str(allow_none=True)
    arbitro_id = fields.Int(allow_none=True)

    @post_load
    def crear_club(self, data, **kwargs):
        return Club(**data)
