from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError

class RegistroSchemaABC(Schema):
    class Meta:
        ordered = True  
    
    solicitud= fields.String(required=False)
    reporteMesa = fields.String(required=False)
    
    nombreRequisitante= fields.String(required=False)
    extensionRequisitante= fields.String(required=False)

    nombreSolicitante= fields.String(required=False)
    puestoSolicitante= fields.String(required=False)   

    nombreAutoriza= fields.String(required=False)
    puestoAutoriza= fields.String(required=False)

    nombreInterno=fields.String(required=False)
    apellidoInterno=fields.String(required=False)
    puestoInterno=fields.String(required=False)
    unidadInterno=fields.String(required=False)
    areaInterno=fields.String(required=False)
    CURPInterno=fields.String(required=False)
    RFCInterno=fields.String(required=False)
    extensionInterno=fields.String(required=False)
    ciudadInterno=fields.String(required=False)
    estadoInterno=fields.String(required=False)
    cpInterno=fields.String(required=False)
    direccionInterno=fields.String(required=False)

    inicioActividades=fields.String(required=False)
    finActividades=fields.String(required=False)
    nombreCuenta=fields.String(required=False)

    justificacion=fields.String(required=False)
    nombreResponsable=fields.String(required=False)
    puestoResponsable=fields.String(required=False)
    ciudadResponsable=fields.String(required=False)
    estadoResponsable=fields.String(required=False)
    cpResponsable=fields.String(required=False)
    direccionResponsable=fields.String(required=False)

    nombreExterno=fields.String(required=False)
    apellidoExterno=fields.String(required=False)
    puestoExterno=fields.String(required=False)
    unidadExterno=fields.String(required=False)
    areaExterno=fields.String(required=False)
    CURPExterno=fields.String(required=False)
    RFCExterno=fields.String(required=False)
    extensionExterno=fields.String(required=False)
    ciudadExterno=fields.String(required=False)
    estadoExterno=fields.String(required=False)
    cpExterno=fields.String(required=False)
    direccionExterno=fields.String(required=False)


    
    