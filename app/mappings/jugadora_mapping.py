from marshmallow import Schema, fields, validate


class JugadoraSchema(Schema):
    id = fields.Str(dump_only=True, attribute='_id')
    nombre = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    apellido = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    dni = fields.Str(required=False, allow_none=True)
    fecha_nacimiento = fields.Str(required=False, allow_none=True)
    categoria = fields.Str(required=False, allow_none=True)
    club_id = fields.Str(required=True)
