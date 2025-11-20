from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError

class RegistroSchemaDNS(Schema):
    class Meta:
        ordered = True
   
    movimiento= fields.String(required=True, validate=validate.OneOf(["ALTA", "BAJA", "CAMBIO"]))
    
    nombreResponsable= fields.String(required=True)
    puestoResponsable = fields.String(required=True)
    
    nombreUsuario= fields.String(required=True)
    areaUsuario= fields.String(required=True)
    puestousuario= fields.String(required=True)
    direccionUsuario= fields.String(required=True)    
    ala= fields.String(required=False)
    piso= fields.String(required=False)
    telefonoUsuario= fields.String(required=False)
    extUsuario= fields.String(required=True)
    
    registro= fields.String(required=True, validate=validate.OneOf(["CNA", "CONAGUA"]))
    nombreRegistro= fields.String(required=False)
    IP= fields.String(required=True)
    nombreAplicacion= fields.String(required=False)
    justificacion= fields.String(required=True,validate=validate.Length(min=20, error="La justificación debe tener mínimo 50 caracteres."))

    fecha= fields.String(required=False)

    nombreAproba= fields.String(required=True)
    puestoAproba= fields.String(required=True)
