from app.models.usuario import Usuario
from marshmallow import Schema, fields

class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    club = fields.Nested(lambda: ClubSchema(only=("id", "nombre")), dump_only=True)
    is_admin = fields.Bool(dump_only=True)


class ClubSchema(Schema):
    id = fields.Int()
    nombre = fields.Str()
