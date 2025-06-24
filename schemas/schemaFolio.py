from marshmallow import Schema, fields, validate

class BusquedaPorFolio(Schema):
    id = fields.String(required=True, validate=validate.Length(10, error="Número de formato inválido"))