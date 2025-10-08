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
    justificacion=fields.String(required=True, validate=validate.Length(min=50, error="La justificación debe tener mínimo 50 caracteres."))

    # Booleanos
    solicitante = fields.String(required=False)
    cuentaUsuario = fields.Boolean(required=False)
    accesoWeb = fields.Boolean(required=False)
    accesoRemoto = fields.Boolean(required=False)
    casoespecial =fields.String(required=False)

    politicasaceptadas = fields.Boolean(required=True)

    # INCISO B)
    registrosWeb = fields.List(fields.Nested(TablasSchemaSitios))
    # INCISO C)
    registrosRemoto = fields.List(fields.Nested(TablasSchemasAcceso))  

    registrosPersonal = fields.List(fields.Nested(TablasSchemaPersonal))

    registrosWebCE = fields.List(fields.Nested(TablasSchemaWebCE))

    @validates_schema
    def validate_servicios_coherencia(self, data, **kwargs):
        errores = {}

        # 1. Validación individual para cada usuario
        for persona_data in data.get('registrosPersonal', []):
            try:
                persona_id = persona_data['id']
                servicios_solicitados = int(persona_data['SERVICIOS'])
            except (KeyError, ValueError):
                # Esto ya debería ser manejado por TablasSchemaPersonal si los campos fueran requeridos.
                # Aquí lo manejamos como un caso donde no se puede verificar la coherencia.
                continue 
            
            servicios_registrados_para_persona = [
                web_ce_data for web_ce_data in data.get('registrosWebCE', [])
                if web_ce_data.get('IDU') == persona_id
            ]
            
            if len(servicios_registrados_para_persona) != servicios_solicitados:
                errores[f'registrosPersonal[{persona_id}]'] = f"El usuario con ID {persona_id} solicitó {servicios_solicitados} servicios, pero se registraron {len(servicios_registrados_para_persona)} servicios en 'registrosWebCE'."

        # 2. Validación de la suma total (opcional, si también quieres esta validación global)
        total_servicios_solicitados = 0
        for persona_data in data.get('registrosPersonal', []):
            try:
                total_servicios_solicitados += int(persona_data.get('SERVICIOS', 0))
            except ValueError:
                # Si 'SERVICIOS' no es un número, ya debería ser manejado por la validación del campo.
                pass

        total_servicios_registrados = len(data.get('registrosWebCE', []))

        if total_servicios_solicitados != total_servicios_registrados:
            errores['general_servicios'] = f"El total de servicios solicitados ({total_servicios_solicitados}) no coincide con el total de servicios registrados en 'registrosWebCE' ({total_servicios_registrados})."
        
        if errores:
            raise ValidationError(errores)
