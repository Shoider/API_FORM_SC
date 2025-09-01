from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError

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
    extEmpleado= fields.String(required=False, validate=validate.Length(min=4, max=20, error="Número/extensión de empleado inválido"))
    #correoEmpleado= fields.Email(required=False, error_messages={"invalid": "Correo electrónico de empleado inválido"})
    correoEmpleado=fields.String(required=False)
    @validates('correoEmpleado')
    def validate_correo_empleado(self, value, **kwargs):
        if value is None or value == "":
            return  # Campo opcional, permite vacío
        if not isinstance(value, str) or not value.lower().endswith("@conagua.gob.mx"):
            raise ValidationError("Debe ser un correo institucional que termine en @conagua.gob.mx.")

    puestoEmpleado= fields.String(required=False, validate=validate.Length(min=1, max=256))

    nombreEnlace= fields.String(required=True, validate=validate.Length(min=1, max=256))
    justificacion = fields.String(required=True, validate=validate.Length(min=50, max=256, error="La justificación debe tener mínimo 50 caracteres."))
    puestoUsuario= fields.String(required=True, validate=validate.Length(min=1, max=256))
    nombreJefe= fields.String(required=True, validate=validate.Length(min=1, max=256))
    puestoJefe= fields.String(required=True, validate=validate.Length(min=1, max=256))
    marca= fields.String(required=False)
    modelo= fields.String(required=False, validate=validate.Length(min=1, max=16))
    serie= fields.String(required=False, validate=validate.Length(min=1, max=16))
    #version= fields.String(required=True, validate=validate.Length(min=1, max=16))
    movimiento= fields.String(required=True, validate=validate.OneOf(["ALTA", "BAJA", "CAMBIO"]))

    mundo= fields.String(required=False, validate=validate.OneOf(["SI", "NO"]))
    nacional= fields.String(required=False, validate=validate.OneOf(["SI", "NO"]))
    celular= fields.String(required=False, validate=validate.OneOf(["SI", "NO"]))

    tipoUsuario= fields.String(required=True)

    fecha= fields.String(required=False)

    politicasaceptadas = fields.Boolean(required=True)

    extinterno=fields.String(required=False, validate=validate.Length(min=1, max=20))