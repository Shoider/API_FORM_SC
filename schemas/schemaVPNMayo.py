from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from schemas.schemaTablasVPN import TablasSchemaSitios
from schemas.schemaTablasVPN import TablasSchemasAcceso

class RegistroSchemaVPNMayo(Schema):

    class Meta:
        ordered = True

    memorando=fields.String(required=False)
    numeroFormato=fields.String(required=False)
    _id=fields.String(required=False)

    unidadAdministrativa = fields.String(required=True)
    areaAdscripcion = fields.String(required=True)
    subgerencia = fields.String(required=True)
    nombreEnlace = fields.String(required=True)
    telefonoEnlace = fields.String(required=True, validate=validate.Length(min=8, max=20, error="Teléfono de enlace/contacto inválido"))
    nombreInterno=fields.String(required=False)
    puestoInterno= fields.String(required=False)
    #correoInterno=fields.String(required=False)
    correoInterno=fields.Email(required=False, error_messages={"invalid": "Correo electrónico inválido"})
    telefonoInterno=fields.String(required=False, validate=validate.Length(min=8, max=20, error="Teléfono de usuario inválido"))
    nombreExterno=fields.String(required=False)
    correoExterno=fields.Email(required=False, error_messages={"invalid": "Correo electrónico inválido"})
    empresaExterno=fields.String(required=False)
    equipoExterno=fields.String(required=False)

    versionSO=fields.String(required=False)

    numeroEmpleadoResponsable=fields.String(required=False, validate=validate.Length(5, error="Número de empleado inválido"))
    
    nombreResponsable=fields.String(required=False)
    puestoResponsable=fields.String(required=False)
    unidadAdministrativaResponsable=fields.String(required=False)
    telefonoResponsable=fields.String(required=False, validate=validate.Length(min=8, max=20, error="Teléfono usuario responsable inválido"))

    tipoEquipo=fields.String(required=True)
    sistemaOperativo=fields.String(required=True)
    marca=fields.String(required=True)
    modelo=fields.String(required=True)
    serie=fields.String(required=True)

    nombreAutoriza=fields.String(required=True)
    puestoAutoriza=fields.String(required=True)

    movimiento =fields.String(required=False)
    justificacion=fields.String(required=True, validate=validate.Length(min=50, max=256, error="La justificación debe tener mínimo 50 caracteres."))

    # Booleanos
    solicitante = fields.String(required=True)
    cuentaUsuario = fields.Boolean(required=True)
    accesoWeb = fields.Boolean(required=True)
    accesoRemoto = fields.Boolean(required=True)

    politicasaceptadas = fields.Boolean(required=True)

    # INCISO B)
    registrosWeb = fields.List(fields.Nested(TablasSchemaSitios))
    # INCISO C)
    registrosRemoto = fields.List(fields.Nested(TablasSchemasAcceso))  
