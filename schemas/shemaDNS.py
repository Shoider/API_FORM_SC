from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError

class RegistroSchemaDNS(Schema):
    
    movimiento= fields.String(required=True)
    
    nombreResponsable= fields.String(required=True)
    puestoResponsable = fields.String(required=True)
    
    nombreUsuario= fields.String(required=True)
    areaUsuario= fields.String(required=True)
    direccionUsuario= fields.String(required=True)    
    ala= fields.String(required=True)
    piso= fields.String(required=True)
    telefonoUsuario= fields.String(required=True)
    extUsuario= fields.String(required=True)
    
    registro= fields.String(required=True)
    nombreRegistro= fields.String(required=True)
    IP= fields.String(required=True)
    nombreAplicacion= fields.String(required=True)
    justificacion= fields.String(required=True)
