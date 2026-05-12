from marshmallow import Schema, fields


class ResultadoSchema(Schema):
    id = fields.Str(dump_only=True, attribute='_id')
    club_local = fields.Str(required=True)
    club_visitante = fields.Str(required=True)
    goles_local = fields.Int(required=True)
    goles_visitante = fields.Int(required=True)
    fecha = fields.Date(required=True)
