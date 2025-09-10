from marshmallow import Schema, fields, validate

from schemas.schemaTablas import TablasSchemaInter
from schemas.schemaTablas import TablasSchemaAdmin

class RegistroSchemaRFC(Schema):

    class Meta:
        ordered = True

    # Datos Generales
    noticket = fields.String(required=False, validate=validate.Length(min=1, max=32))
    memo = fields.String(required=True, validate=validate.Length(min=1, max=256))
    descbreve = fields.String(required=True, validate=validate.Length(min=1, max=256))
    _id = fields.String(required=False)

    nomei = fields.String(required=False)
    extei = fields.String(required=False, validate=validate.Length(min=4, max=20, error="Teléfono/extensión de enlace informático inválido"))

    #BOOLEANO
    politicasaceptadas = fields.Boolean(required=True)

    noms = fields.String(required=False)
    exts = fields.String(required=False, validate=validate.Length(min=4, max=20, error="Teléfono/extensión de solicitante inválido"))
    puestos = fields.String(required=False)
    areas = fields.String(required=False)
    nombreJefe = fields.String(required=True)
    puestoJefe = fields.String(required=True)
    
    desdet = fields.String(required=True, validate=validate.Length(min=40, max=256, error="La descripción detallada ingresada es muy breve."))
    desotro = fields.String(required=False)
    
    #AQUI NO REQUIERE QUE VALIDE LAS TRES, SOLO DEBE DE TENER ALGUNA 
    justifica = fields.String(required=False)
    justifica2 = fields.String(required=False)
    justifica3 = fields.String(required=False) 

    # Quien lo solicita
    #soli = fields.Boolean(required=False)
    #enlace = fields.Boolean(required=False)
    region = fields.String(required=True) 

    # Tablas y Tipos de Cambio #

    # Tipos de Cambios
    intersistemas = fields.Boolean(required=False)
    administrador = fields.Boolean(required=False)
    desarrollador = fields.Boolean(required=False)
    usuario = fields.Boolean(required=False)
    otro = fields.Boolean(required=False)

    # Tipo de movimiento
    # InterSistemas
    AltaInter = fields.Boolean(required=False)
    BajaInter = fields.Boolean(required=False)
    CambioInter = fields.Boolean(required=False)
    # Administrador
    AltaAdmin = fields.Boolean(required=False)
    BajaAdmin = fields.Boolean(required=False)
    CambioAdmin = fields.Boolean(required=False)
    # Desarrollador
    AltaDes = fields.Boolean(required=False)
    BajaDes = fields.Boolean(required=False)
    CambioDes = fields.Boolean(required=False)
    # Usuario
    AltaUsua = fields.Boolean(required=False)
    BajaUsua = fields.Boolean(required=False)
    CambioUsua = fields.Boolean(required=False)
    # Otro
    AltaOtro = fields.Boolean(required=False)
    BajaOtro = fields.Boolean(required=False)
    CambioOtro = fields.Boolean(required=False)

    # Tablas
    # InterSistemas
    registrosInterAltas = fields.List(fields.Nested(TablasSchemaInter))
    registrosInterBajas = fields.List(fields.Nested(TablasSchemaInter))
    registrosInterCambiosAltas = fields.List(fields.Nested(TablasSchemaInter))
    registrosInterCambiosBajas = fields.List(fields.Nested(TablasSchemaInter))
    # Administrador
    registrosAdminAltas = fields.List(fields.Nested(TablasSchemaAdmin))
    registrosAdminBajas = fields.List(fields.Nested(TablasSchemaAdmin))
    registrosAdminCambiosAltas = fields.List(fields.Nested(TablasSchemaAdmin))
    registrosAdminCambiosBajas = fields.List(fields.Nested(TablasSchemaAdmin))
    # Desarrollador
    registrosDesAltas = fields.List(fields.Nested(TablasSchemaAdmin))
    registrosDesBajas = fields.List(fields.Nested(TablasSchemaAdmin))
    registrosDesCambiosAltas = fields.List(fields.Nested(TablasSchemaAdmin))
    registrosDesCambiosBajas = fields.List(fields.Nested(TablasSchemaAdmin))
    # Usuario
    registrosUsuaAltas = fields.List(fields.Nested(TablasSchemaAdmin))
    registrosUsuaBajas = fields.List(fields.Nested(TablasSchemaAdmin))
    registrosUsuaCambiosAltas = fields.List(fields.Nested(TablasSchemaAdmin))
    registrosUsuaCambiosBajas = fields.List(fields.Nested(TablasSchemaAdmin))
    # Otro
    registrosOtroAltas = fields.List(fields.Nested(TablasSchemaAdmin))
    registrosOtroBajas = fields.List(fields.Nested(TablasSchemaAdmin))
    registrosOtroCambiosAltas = fields.List(fields.Nested(TablasSchemaAdmin))
    registrosOtroCambiosBajas = fields.List(fields.Nested(TablasSchemaAdmin))