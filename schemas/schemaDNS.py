from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError

class RegistroSchemaDNS(Schema):
    _id=fields.String(required=False)
    movimiento= fields.String(required=False, validate=validate.OneOf(["ALTA", "BAJA", "CAMBIO"]))
    
    nombreResponsable= fields.String(required=False)
    puestoResponsable = fields.String(required=False)
    
    nombreUsuario= fields.String(required=False)
    areaUsuario= fields.String(required=False)
    puestoUsuario= fields.String(required=False)
    direccionUsuario= fields.String(required=False)    
    ala= fields.String(required=False)
    piso= fields.String(required=False)
    telefonoUsuario= fields.String(required=False)
    extUsuario= fields.String(required=False)
    
    registro= fields.String(required=False, validate=validate.OneOf(["CNA", "CONAGUA"]))
    nombreRegistro= fields.String(required=False)
    IP= fields.String(required=False)
    nombreAplicacion= fields.String(required=False)
    justificacion= fields.String(required=False)

    fecha= fields.String(required=False)

    nombreAproba= fields.String(required=False)
    puestoAproba= fields.String(required=False)
