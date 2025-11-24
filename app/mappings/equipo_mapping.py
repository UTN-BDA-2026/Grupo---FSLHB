from marshmallow import Schema, fields, post_load
from app.models.equipo import Equipo

class EquipoSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    categoria = fields.Str(required=False, allow_none=True)
    club_id = fields.Int(required=True)

    @post_load
    def crear_equipo(self, data, **kwargs):
        return Equipo(**data)
