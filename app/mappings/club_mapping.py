from marshmallow import Schema, fields, validate


class ClubMapping(Schema):
    id = fields.Str(dump_only=True, attribute='_id')
    nombre = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    razon_social = fields.Str(allow_none=True)
    contacto = fields.Str(allow_none=True)
    email = fields.Str(allow_none=True)
    cancha_local = fields.Str(allow_none=True)
    domicilio = fields.Str(allow_none=True)
    telefono = fields.Str(allow_none=True)
    web = fields.Str(allow_none=True)
    arbitro_id = fields.Str(allow_none=True)
