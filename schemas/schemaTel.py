from marshmallow import Schema, fields, validate

class RegistroSchemaTel(Schema):
    
    activacion= fields.String(required=True)
    expiracion= fields.String(required=True)
    nombreUsuario = fields.String(required=True, validate=validate.Length(min=1, max=256))
    correoUsuario = fields.Email(required=False, error_messages={"invalid": "Correo electrónico de usuario inválido"})
    direccion= fields.String(required=True)
    piso= fields.String(required=False)
    ala= fields.String(required=False)
    uaUsuario= fields.String(required=True)

    nombreEmpleado= fields.String(required=False, validate=validate.Length(min=1, max=256))
    idEmpleado= fields.String(required=False, validate=validate.Length(5, error="Número de empleado inválido"))
    extEmpleado= fields.String(required=False, validate=validate.Length(min=1, max=20))
    correoEmpleado= fields.Email(required=False, error_messages={"invalid": "Correo electrónico de empleado inválido"})
    puestoEmpleado= fields.String(required=False, validate=validate.Length(min=1, max=256))

    nombreEnlace= fields.String(required=True, validate=validate.Length(min=1, max=256))
    justificacion = fields.String(required=True, validate=validate.Length(min=50, max=256, error="La justificación debe tener mínimo 50 caracteres."))
    puestoUsuario= fields.String(required=True, validate=validate.Length(min=1, max=256))
    nombreJefe= fields.String(required=True, validate=validate.Length(min=1, max=256))
    puestoJefe= fields.String(required=True, validate=validate.Length(min=1, max=256))
    marca= fields.String(required=True)
    modelo= fields.String(required=True, validate=validate.Length(min=1, max=16))
    serie= fields.String(required=True, validate=validate.Length(min=1, max=16))
    #version= fields.String(required=True, validate=validate.Length(min=1, max=16))
    movimiento= fields.String(required=True, validate=validate.OneOf(["ALTA", "BAJA", "CAMBIO"]))

    mundo= fields.String(required=True, validate=validate.OneOf(["SI", "NO"]))
    nacional= fields.String(required=True, validate=validate.OneOf(["SI", "NO"]))
    celular= fields.String(required=True, validate=validate.OneOf(["SI", "NO"]))

    tipoUsuario= fields.String(required=True)

    usuaExterno= fields.Boolean(required=False)
    fecha= fields.String(required=False)

    politicasaceptadas = fields.Boolean(required=True)