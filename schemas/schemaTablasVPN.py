from marshmallow import Schema, fields, validate, validates, ValidationError
import ipaddress
import re

class TablasSchemaSitios(Schema):
    id=fields.Integer(required=False)
    movimiento=fields.String(required=False)
    nombreSistema=fields.String(required=False)
    siglas=fields.String(required=False)
    url=fields.String(required=False)

    @validates('url')
    def validate_url_or_ip(self, value, **kwargs):
        if value is None or value == "":
            return  # Campo opcional, permite vacío

        # Si comienza con http o https, es válido
        if value.lower().startswith("http"):
            return

        # Si es una IP válida y comienza con 172.
        try:
            ip = ipaddress.ip_address(value)
            if str(ip).startswith("172."):
                return
        except ValueError:
            pass  # No es una IP, continuar

        raise ValidationError("Debe comenzar con 'http' o ser una IP que inicie con '172.'")
     
    puertosServicios=fields.String(required=False)
    isNew=fields.Boolean(required=False)
     
class TablasSchemasAcceso (Schema):
    id =fields.Integer(required=False)
    movimiento =fields.String(required=False)
    nomenclatura =fields.String(required=False, validate=validate.Length(min=8))

    nombreSistema =fields.String(required=False, validate=validate.Length(min=11))
        
    direccion =fields.String(required=False)

    @validates('direccion')
    def validate_url_or_ip(self, value, **kwargs):
        if value is None:
            # Si el campo es opcional y no se proporciona, no hay nada que validar
            return
        # Intentar validar como IP
        try:
            ip = ipaddress.ip_address(value)
            if str(ip).startswith("172."):
                return  # Es una IP válida
        except ValueError:
            pass  # No es una IP, continuar con otras validaciones
        # Si ninguna de las anteriores coincide, lanza un error
        raise ValidationError("Debe ser una IP que inicie con '172..")
    sistemaOperativo =fields.String(required=False)
    isNew=fields.Boolean(required=False)
    
    
class TablasSchemaPersonal(Schema):
    id= fields.Integer(required=False)
    NOMBRE = fields.String(required=False)
    CORREO = fields.String(required=False)
    @validates('CORREO')
    def validate_email(self, value, **kwargs):
        if value is None or value == "":
            return  # Campo opcional, permite vacío
        # Validación básica de correo electrónico
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, value):
            raise ValidationError("Formato de correo inválido en tabla.")
    
    EMPRESA = fields.String(required=False)
    EQUIPO = fields.String(required=False)
    SERVICIOS = fields.Integer(required=False)
    isNew=fields.Boolean(required=False)

class TablasSchemaWebCE (Schema):
    id = fields.Integer(required=False)
    IDU = fields.Integer(required=False)
    NOMBRE = fields.String(required=False)
    SIGLAS = fields.String(required=False)
    URL = fields.String(required=False)
    @validates('URL')
    def validate_url_or_ip(self, value, **kwargs):
        if value is None or value == "":
            return  # Campo opcional, permite vacío
        
        # No permite que tenga espaciados para evitar que pongan más de una
        if " " in value:
            raise ValidationError("No se permite más de una URL/IP.")

        # Si comienza con http o https, es válido
        if value.lower().startswith("http"):
            return

        # Si es una IP válida y comienza con 172.
        try:
            ip = ipaddress.ip_address(value)
            if str(ip).startswith("172."):
                return
        except ValueError:
            pass  # No es una IP, continuar

        raise ValidationError("Formato de URL/IP inválido en tabla.")
    PUERTOS =fields.String(required=False)
    isNew=fields.Boolean(required=False)
     
    
