from marshmallow import Schema, fields, validate, validates, ValidationError
import ipaddress

# Definimos la lógica UNA SOLA VEZ en una función.
def validar_formato_url(value):
    """
    Validador reutilizable que comprueba si un valor (que no sea vacío)
    comienza con 'http'.
    """
    # Si el campo es opcional y viene vacío, es válido.
    if not value: # Esto cubre None, "" y otros valores "falsy".
        return

    if not isinstance(value, str) or not value.lower().startswith("http"):
        raise ValidationError("El campo debe ser una URL válida que comience con 'http'.")
    
def validar_ip_interna(value):
    """
    Validador reutilizable que comprueba si un valor es una IP
    que comienza con "172.".
    """
    try:
        ip = ipaddress.ip_address(value)
        if str(ip).startswith("172."):
            return  # Es una IP válida que cumple la condición
    except ValueError:
        # Si no es una IP válida, dejamos que lance el error al final.
        pass

    # Nota: Corregí el doble punto ".." al final de tu mensaje de error original.
    raise ValidationError("Debe ser una dirección IP válida que inicie con '172.'.")

class RegistroSchemaInter(Schema):

    class Meta:
        ordered = True
        
    fechasoli = fields.String(required=True)
    uaUsuario= fields.String(required=True)
    areaUsuario= fields.String(required=True)
    nombreUsuario= fields.String(required=True)
    puestoUsuario= fields.String(required=True)
    ipUsuario = fields.String(required=True, validate=validar_ip_interna)
    correoUsuario=fields.Email(required=False, error_messages={"invalid": "Correo electrónico inválido"})
    direccion= fields.String(required=True)
    teleUsuario= fields.Number(required=True, error_messages={"invalid": "Teléfono de usuario inválido"})
    extUsuario= fields.String(required=True, validate=validate.Length(4, error="Número de extensión inválido"))
    nombreJefe= fields.String(required=True)
    puestoJefe= fields.String(required=True)

    descarga= fields.Boolean(required=True)
    comercio= fields.Boolean(required=True)
    redes= fields.Boolean(required=True)
    foros= fields.Boolean(required=True)
    whats= fields.Boolean(required=True)
    videos= fields.Boolean(required=True)
    dropbox= fields.Boolean(required=True)
    skype= fields.Boolean(required=True)
    wetransfer= fields.Boolean(required=True)
    team= fields.Boolean(required=True)
    otra= fields.Boolean(required=True)
    otra2= fields.Boolean(required=False)
    otra3= fields.Boolean(required=False)
    otra4= fields.Boolean(required=False)
    onedrive= fields.Boolean(required=True)

    urlDescarga = fields.String(required=False, allow_none=True, validate=validar_formato_url)
    
    justificaDescarga = fields.String(required=False, validate=validate.Length(min=50, max=256, error="La justificación debe tener mínimo 50 caracteres."))
    urlForos = fields.String(required=False, allow_none=True, validate=validar_formato_url)

    justificaForos= fields.String(required=False, validate=validate.Length(min=50, max=256, error="La justificación debe tener mínimo 50 caracteres."))
    urlComercio= fields.String(required=False, allow_none=True, validate=validar_formato_url)
    justificaComercio= fields.String(required=False, validate=validate.Length(min=50, max=256, error="La justificación debe tener mínimo 50 caracteres."))
    urlRedes= fields.String(required=False, allow_none=True, validate=validar_formato_url)
    justificaRedes= fields.String(required=False, validate=validate.Length(min=50, max=256, error="La justificación debe tener mínimo 50 caracteres."))
    urlVideos= fields.String(required=False, allow_none=True, validate=validar_formato_url)
    justificaVideos= fields.String(required=False, validate=validate.Length(min=50, max=256, error="La justificación debe tener mínimo 50 caracteres."))
    urlWhats= fields.String(required=False, allow_none=True, validate=validar_formato_url)
    justificaWhats= fields.String(required=False, validate=validate.Length(min=50, max=256, error="La justificación debe tener mínimo 50 caracteres."))
    urlDropbox= fields.String(required=False, allow_none=True, validate=validar_formato_url)
    justificaDropbox= fields.String(required=False, validate=validate.Length(min=50, max=256, error="La justificación debe tener mínimo 50 caracteres."))
    urlOnedrive= fields.String(required=False, allow_none=True, validate=validar_formato_url)
    justificaOnedrive= fields.String(required=False, validate=validate.Length(min=50, max=256, error="La justificación debe tener mínimo 50 caracteres."))
    urlSkype= fields.String(required=False, allow_none=True, validate=validar_formato_url)
    justificaSkype= fields.String(required=False, validate=validate.Length(min=50, max=256, error="La justificación debe tener mínimo 50 caracteres."))
    urlWetransfer= fields.String(required=False, allow_none=True, validate=validar_formato_url)
    justificaWetransfer= fields.String(required=False, validate=validate.Length(min=50, max=256, error="La justificación debe tener mínimo 50 caracteres."))
    urlTeam= fields.String(required=False, allow_none=True, validate=validar_formato_url)
    justificaTeam= fields.String(required=False, validate=validate.Length(min=50, max=256, error="La justificación debe tener mínimo 50 caracteres."))
    urlOtra= fields.String(required=False, allow_none=True, validate=validar_formato_url)
    justificaOtra= fields.String(required=False, validate=validate.Length(min=50, max=256, error="La justificación debe tener mínimo 50 caracteres."))
    otraC= fields.String(required=False)
    urlOtra2= fields.String(required=False, allow_none=True, validate=validar_formato_url)
    justificaOtra2= fields.String(required=False, validate=validate.Length(min=50, max=256, error="La justificación debe tener mínimo 50 caracteres."))
    otraC2= fields.String(required=False)
    urlOtra3= fields.String(required=False, allow_none=True, validate=validar_formato_url)
    justificaOtra3= fields.String(required=False, validate=validate.Length(min=50, max=256, error="La justificación debe tener mínimo 50 caracteres."))
    otraC3= fields.String(required=False)
    urlOtra4= fields.String(required=False, allow_none=True, validate=validar_formato_url)
    justificaOtra4= fields.String(required=False, validate=validate.Length(min=50, max=256, error="La justificación debe tener mínimo 50 caracteres."))
    otraC4= fields.String(required=False)

    ala= fields.String(required=False)
    piso= fields.String(required=False)

    politicasaceptadas = fields.Boolean(required=True)


    
