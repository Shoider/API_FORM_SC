from marshmallow import Schema, fields, validates, ValidationError
import ipaddress

class RegistroSchemaInter(Schema):

    class Meta:
        ordered = True

    fechasoli = fields.String(required=True)
    uaUsuario= fields.String(required=True)
    areaUsuario= fields.String(required=True)
    nombreUsuario= fields.String(required=True)
    puestoUsuario= fields.String(required=True)
    ipUsuario= fields.String(required=True)
    @validates('ipUsuario')
    def validate_url_or_ip(self, value):
        # Intentar validar como IP
        try:
            ip = ipaddress.ip_address(value)
            if str(ip).startswith("172."):
                return  # Es una IP válida
        except ValueError:
            pass  # No es una IP, continuar con otras validaciones
        # Si ninguna de las anteriores coincide, lanza un error
        raise ValidationError("Debe ser una IP que inicie con '172..")
    
    correoUsuario=fields.Email(required=False, error_messages={"invalid": "Correo electrónico inválido"})
    direccion= fields.String(required=True)
    teleUsuario= fields.String(required=True)
    extUsuario= fields.String(required=True)
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

    urlDescarga= fields.String(required=False)
    @validates('urlDescarga')
    def validate_url(self, value):
        if value is None or value == "":
            return  # Campo opcional, permite vacío
        if value.lower().startswith("http"):
            return
        raise ValidationError("Debe comenzar con 'http'")
    
    justificaDescarga= fields.String(required=False)
    urlForos= fields.String(required=False)
    @validates('urlForos')
    def validate_url(self, value):
        if value is None or value == "":
            return  # Campo opcional, permite vacío
        if value.lower().startswith("http"):
            return
        raise ValidationError("Debe comenzar con 'http'")
    justificaForos= fields.String(required=False)
    urlComercio= fields.String(required=False)
    @validates('urlComercio')
    def validate_url(self, value):
        if value is None or value == "":
            return  # Campo opcional, permite vacío
        if value.lower().startswith("http"):
            return
        raise ValidationError("Debe comenzar con 'http'")
    justificaComercio= fields.String(required=False)
    urlRedes= fields.String(required=False)
    @validates('urlRedes')
    def validate_url(self, value):
        if value is None or value == "":
            return  # Campo opcional, permite vacío
        if value.lower().startswith("http"):
            return
        raise ValidationError("Debe comenzar con 'http'")
    justificaRedes= fields.String(required=False)
    urlVideos= fields.String(required=False)
    @validates('urlVideos')
    def validate_url(self, value):
        if value is None or value == "":
            return  # Campo opcional, permite vacío
        if value.lower().startswith("http"):
            return
        raise ValidationError("Debe comenzar con 'http'")
    justificaVideos= fields.String(required=False)
    urlWhats= fields.String(required=False)
    @validates('urlWhats')
    def validate_url(self, value):
        if value is None or value == "":
            return  # Campo opcional, permite vacío
        if value.lower().startswith("http"):
            return
        raise ValidationError("Debe comenzar con 'http'")
    justificaWhats= fields.String(required=False)
    urlDropbox= fields.String(required=False)
    @validates('urlDropbox')
    def validate_url(self, value):
        if value is None or value == "":
            return  # Campo opcional, permite vacío
        if value.lower().startswith("http"):
            return
        raise ValidationError("Debe comenzar con 'http'")
    justificaDropbox= fields.String(required=False)
    urlOnedrive= fields.String(required=False)
    @validates('urlOnedrive')
    def validate_url(self, value):
        if value is None or value == "":
            return  # Campo opcional, permite vacío
        if value.lower().startswith("http"):
            return
        raise ValidationError("Debe comenzar con 'http'")
    justificaOnedrive= fields.String(required=False)
    urlSkype= fields.String(required=False)
    @validates('urlSkype')
    def validate_url(self, value):
        if value is None or value == "":
            return  # Campo opcional, permite vacío
        if value.lower().startswith("http"):
            return
        raise ValidationError("Debe comenzar con 'http'")
    justificaSkype= fields.String(required=False)
    urlWetransfer= fields.String(required=False)
    @validates('urlWetransfer')
    def validate_url(self, value):
        if value is None or value == "":
            return  # Campo opcional, permite vacío
        if value.lower().startswith("http"):
            return
        raise ValidationError("Debe comenzar con 'http'")
    justificaWetransfer= fields.String(required=False)
    urlTeam= fields.String(required=False)
    @validates('urlTeam')
    def validate_url(self, value):
        if value is None or value == "":
            return  # Campo opcional, permite vacío
        if value.lower().startswith("http"):
            return
        raise ValidationError("Debe comenzar con 'http'")
    justificaTeam= fields.String(required=False)
    urlOtra= fields.String(required=False)
    @validates('urlOtra')
    def validate_url(self, value):
        if value is None or value == "":
            return  # Campo opcional, permite vacío
        if value.lower().startswith("http"):
            return
        raise ValidationError("Debe comenzar con 'http'")
    justificaOtra= fields.String(required=False)
    otraC= fields.String(required=False)
    urlOtra2= fields.String(required=False)
    @validates('urlOtra2')
    def validate_url(self, value):
        if value is None or value == "":
            return  # Campo opcional, permite vacío
        if value.lower().startswith("http"):
            return
        raise ValidationError("Debe comenzar con 'http'")
    justificaOtra2= fields.String(required=False)
    otraC2= fields.String(required=False)
    urlOtra3= fields.String(required=False)
    @validates('urlOtra3')
    def validate_url(self, value):
        if value is None or value == "":
            return  # Campo opcional, permite vacío
        if value.lower().startswith("http"):
            return
        raise ValidationError("Debe comenzar con 'http'")
    justificaOtra3= fields.String(required=False)
    otraC3= fields.String(required=False)
    urlOtra4= fields.String(required=False)
    @validates('urlOtra4')
    def validate_url(self, value):
        if value is None or value == "":
            return  # Campo opcional, permite vacío
        if value.lower().startswith("http"):
            return
        raise ValidationError("Debe comenzar con 'http'")
    justificaOtra4= fields.String(required=False)
    otraC4= fields.String(required=False)

    ala= fields.String(required=False)
    piso= fields.String(required=False)

    politicasaceptadas = fields.Boolean(required=True)


    
