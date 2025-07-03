from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from schemas.schemaTablasVPN import TablasSchemaSitios
from schemas.schemaTablasVPN import TablasSchemasAcceso

from schemas.schemaTablasVPN import TablasSchemaPersonal
from schemas.schemaTablasVPN import TablasSchemaWebCE


class RegistroSchemaVPNMayo(Schema):

    class Meta:
        ordered = True

    memorando=fields.String(required=False)
    numeroFormato=fields.String(required=False)
    _id=fields.String(required=False)

    fecha=fields.String(required=False)
    epoch=fields.Integer(required=False)

    unidadAdministrativa = fields.String(required=True)
    areaAdscripcion = fields.String(required=True)
    subgerencia = fields.String(required=True)
    nombreEnlace = fields.String(required=True)
    puestoEnlace = fields.String(required=False)
    telefonoEnlace = fields.String(required=True, validate=validate.Length(min=8, max=20, error="Teléfono de enlace/contacto inválido"))
    nombreInterno=fields.String(required=False)
    puestoInterno= fields.String(required=False)
    #correoInterno=fields.String(required=False)
    correoInterno=fields.String(required=False)
    @validates('correoInterno')
    def validate_correo_interno(self, value, **kwargs):
        if value is None or value == "":
            return  # Campo opcional, permite vacío
        if not isinstance(value, str) or not value.lower().endswith("@conagua.gob.mx"):
            raise ValidationError("Debe ser un correo institucional que termine en @conagua.gob.mx.")
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

    tipoEquipo=fields.String(required=False)
    sistemaOperativo=fields.String(required=False)
    marca=fields.String(required=False)
    modelo=fields.String(required=False)
    serie=fields.String(required=False)

    nombreAutoriza=fields.String(required=False)
    puestoAutoriza=fields.String(required=False)

    movimiento =fields.String(required=False)
    justificacion=fields.String(required=True, validate=validate.Length(min=50, max=256, error="La justificación debe tener mínimo 50 caracteres."))

    # Booleanos
    solicitante = fields.String(required=False)
    cuentaUsuario = fields.Boolean(required=False)
    accesoWeb = fields.Boolean(required=False)
    accesoRemoto = fields.Boolean(required=False)

    politicasaceptadas = fields.Boolean(required=True)

    # INCISO B)
    registrosWeb = fields.List(fields.Nested(TablasSchemaSitios))
    # INCISO C)
    registrosRemoto = fields.List(fields.Nested(TablasSchemasAcceso))  

    registrosPersonal = fields.List(fields.Nested(TablasSchemaPersonal))

    registrosWebCE = fields.List(fields.Nested(TablasSchemaWebCE))
