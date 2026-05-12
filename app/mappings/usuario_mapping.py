from marshmallow import Schema, fields


class UsuarioSchema(Schema):
    id = fields.Str(dump_only=True, attribute='_id')
    username = fields.Str(required=True)
    club = fields.Nested(lambda: ClubSchema(only=("id", "nombre")), dump_only=True)
    is_admin = fields.Bool(dump_only=True)
    is_operador = fields.Bool(dump_only=True)
    puede_cargar_incidencias = fields.Bool(dump_only=True)
    puede_precargar_equipos = fields.Bool(dump_only=True)


class ClubSchema(Schema):
    id = fields.Str(attribute='_id')
    nombre = fields.Str()
