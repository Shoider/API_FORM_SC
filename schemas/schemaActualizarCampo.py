from marshmallow import Schema, fields, validate

class ActualizacionCampo(Schema):
    noticket=fields.String(required=False)
    memorando=fields.String(required=False)
    numeroFormato=fields.String(required=True)