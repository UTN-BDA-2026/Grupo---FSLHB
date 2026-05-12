from marshmallow import Schema, fields


class EquipoSchema(Schema):
    id = fields.Str(dump_only=True, attribute='_id')
    nombre = fields.Str(required=True)
    categoria = fields.Str(required=False, allow_none=True)
    club_id = fields.Str(required=True)
