from flask import Blueprint, request, jsonify, send_file
from logger.logger import Logger
from marshmallow import ValidationError
import time

class FileGeneratorRoute(Blueprint):
    """Class to handle the routes for file generation"""

    def __init__(self, service, forms_schemaVPNMayo, forms_schemaTel, forms_schemaRFC, form_schemaInter, form_schemaFolio, form_schemaCampo):
        super().__init__("file_generator", __name__)
        self.logger = Logger()
        self.forms_schemaVPNMayo = forms_schemaVPNMayo
        self.forms_schemaTel = forms_schemaTel
        self.forms_schemaRFC = forms_schemaRFC
        self.form_schemaInter = form_schemaInter
        self.form_schemaFolio = form_schemaFolio
        self.form_schemaCampo = form_schemaCampo
        self.service = service
        self.register_routes()

    def register_routes(self):
        """Function to register the routes for file generation"""
        self.route("/api2/v3/vpn", methods=["POST"])(self.vpnmayo)
        self.route("/api2/v3/vpnActualizar", methods=["POST"])(self.vpnMemorando)
        self.route("/api2/v3/telefonia", methods=["POST"])(self.telefonia)
        self.route("/api2/v3/internet", methods=["POST"])(self.internet)
        self.route("/api2/v3/rfc", methods=["POST"])(self.rfc)
        self.route("/api2/v3/rfcActualizar", methods=["POST"])(self.rfcTicket)
        self.route("/api2/v3/folio", methods=["POST"])(self.busquedaFolio)
        self.route("/api2/healthcheck", methods=["GET"])(self.healthcheck)

    def fetch_request_data(self):
        """Function to fetch the request data"""
        try:
            request_data = request.json
            if not request_data:
                return 400, "Invalid data", None
            return 200, None, request_data
        except Exception as e:
            self.logger.error(f"Error fetching request data: {e}")
            return 500, "Error fetching request data", None
        
    def eliminar_campos_vacios(self, datos):
        """
        Elimina recursivamente los campos (pares clave-valor) de los diccionarios
        donde el valor es una cadena vacía ("") ó ("null").

        Procesa diccionarios anidados y diccionarios dentro de listas.
        Las cadenas vacías que sean elementos directos de una lista (ej: ["a", "", "b"])
        NO se eliminan de la lista, ya que no son "campos" de un diccionario.
        Otros tipos de datos (números, booleanos, None, cadenas no vacías) se conservan.

        Args:
            datos: Puede ser un diccionario o una lista para limpiar.

        Returns:
            Una nueva estructura de datos (diccionario o lista) sin los campos
            que contenían cadenas vacías.
        """
        if isinstance(datos, dict):
            # Crear un nuevo diccionario para los datos limpios
            diccionario_limpio = {}
            for clave, valor in datos.items():
                if valor == "":
                    # Si el valor es una cadena vacía, omitir este campo
                    continue
                if valor == "null":
                    continue
                elif isinstance(valor, dict):
                    # Si el valor es un diccionario, aplicar la función recursivamente
                    diccionario_limpio[clave] = self.eliminar_campos_vacios(valor)
                elif isinstance(valor, list):
                    # Si el valor es una lista, aplicar la función recursivamente a cada elemento
                    diccionario_limpio[clave] = [self.eliminar_campos_vacios(item) for item in valor]
                else:
                    # Para cualquier otro valor, conservarlo
                    diccionario_limpio[clave] = valor
            return diccionario_limpio
        elif isinstance(datos, list):
            # Si la estructura de datos es una lista, aplicar la función a cada elemento
            return [self.eliminar_campos_vacios(item) for item in datos]
        else:
            # Si no es un diccionario ni una lista (ej: string, int, None), devolverlo tal cual
            return datos

    def vpnmayo(self):
        """
        Esta ruta es para validar todos los datos ingresados y resppnder rapidamente en caso de error,
        es mas ligera que la que genera el pdf.
        Es probable que se guarde todo en la base de datos bajo un token y despues este
        se llame para generar el pdf.

        Args:
            data: Un diccionario.

        Returns:
            Token con id de la base de datos.
            Errores de validacion.
        """
        try:

            # Validacion de datos recibidos
            data = request.get_json()
            if not data:
                return jsonify({"error": "No se enviaron datos"}), 400
            
            # Preparacion de datos para validar
            datosProcesados = self.eliminar_campos_vacios(data)
            self.logger.info(f"Datos despues de limpieza: {datosProcesados}")

            # Validacion de los datos en schema
            self.forms_schemaVPNMayo.load(datosProcesados)
            self.logger.info("Ya se validaron correctamente")

            # Guardar en base de datos
            # Llamar al servicio y retornar el id
            vpnmayo_registro, status_code = self.service.add_VPNMayo(datosProcesados)

            if status_code == 201:
                noformato = vpnmayo_registro.get('_id')
                epoch = vpnmayo_registro.get('epoch')
                self.logger.info(f"Registro VPN Mayo agregado con ID: {noformato}")

                # Enviar informacion al frontend
                return jsonify({"message": "Generando PDF", "id": noformato, "epoch": epoch}), 200
            else:
                self.logger.error(f"Error agregando el registro a la base de datos")
                # Enviar informacion al frontend
                return jsonify({"error": "Error agregando el registro a la base de datos"}), 500
            
        except ValidationError as err:
            messages = err.messages
            self.logger.warning("Ocurrieron errores de validación")
            self.logger.info(f"Errores de validación completos: {messages}")

            # REGISTROS WEB B)
            if 'registrosWeb' in messages:
                web = messages['registrosWeb']
                if isinstance(web, dict):
                    for indice_item_str, errores_del_item in web.items():
                        # url
                        if isinstance(errores_del_item, dict) and 'url' in errores_del_item:
                            self.logger.error(f"Error de validación: 'url'")
                            return jsonify({"error": "Datos invalidos", "message": "b) Verifica 'URL/IP del Equipo'"}), 422
                        # nombreSistema
                        if isinstance(errores_del_item, dict) and 'nombreSistema' in errores_del_item:
                            self.logger.error(f"Error de validación: 'nombreSistema'")
                            return jsonify({"error": "Datos invalidos", "message": "b) Verifica 'Nombre Sistema/Servicio'"}), 422
            
            # REGISTROS REMOTO C)
            if 'registrosRemoto' in messages:
                remoto = messages['registrosRemoto']
                if isinstance(remoto, dict):
                    for indice_item_str, errores_del_item in remoto.items():
                        # nomeclatura
                        if isinstance(errores_del_item, dict) and 'nomenclatura' in errores_del_item:
                            self.logger.error(f"Error de validación: 'nomenclatura'")
                            return jsonify({"error": "Datos invalidos", "message": "c) Verifica 'Nomenclatura'. Min: 8 Caracteres"}), 422
                        # nombreSistema
                        if isinstance(errores_del_item, dict) and 'nombreSistema' in errores_del_item:
                            self.logger.error(f"Error de validación: 'nombreSistema'")
                            return jsonify({"error": "Datos invalidos", "message": "c) Verifica 'Nombre'. Min: 11 Caracteres"}), 422
                        # direccion
                        if isinstance(errores_del_item, dict) and 'direccion' in errores_del_item:
                            self.logger.error(f"Error de validación: 'direccion'")
                            return jsonify({"error": "Datos invalidos", "message": "c) Verifica 'Dirección IP'"}), 422
                        
            # REGISTROS Personal
            if 'registrosPersonal' in messages:
                remoto = messages['registrosPersonal']
                if isinstance(remoto, dict):
                    for indice_item_str, errores_del_item in remoto.items():
                        # CORREO
                        if isinstance(errores_del_item, dict) and 'CORREO' in errores_del_item:
                            self.logger.error(f"Error de validación: 'CORREO'")
                            return jsonify({"error": "Datos invalidos", "message": " Verifica 'Correo Electrónico' de la tabla", "campo": "registrosPersonal"}), 422
            # REGISTROS WebCE
            if 'registrosWebCE' in messages:
                remoto = messages['registrosWebCE']
                if isinstance(remoto, dict):
                    for indice_item_str, errores_del_item in remoto.items():
                        # URL
                        if isinstance(errores_del_item, dict) and 'URL' in errores_del_item:
                            self.logger.error(f"Error de validación: 'URL'")
                            return jsonify({"error": "Datos invalidos", "message": " Verifica el formato de 'URL/IP' de la tabla o asegurate que sea uno por renglón",  "campo": "registrosWebCE"}), 422
            
            # VALICACION SERVICIOS                        
            for key, value in messages.items():
                if key.startswith('registrosPersonal[') and isinstance(value, str): # Error individual por ID de usuario
                    self.logger.error(f"Error de validación de servicios por usuario: '{key}'")
                    return jsonify({"error": "Datos inválidos", "message": f"Verifica la cantidad de servicios registrados para el usuario con IDU {key.split('[')[1][:-1]}", "campo": "registrosWebCE"}), 422
                elif key == 'general_servicios' and isinstance(value, str): # Error de suma total
                    self.logger.error(f"Error de validación de suma total de servicios: '{key}'")
                    return jsonify({"error": "Datos inválidos", "message": "El número total de servicios solicitados no coincide con los servicios registrados", "campo": "registrosWebCE"}), 422
                
            # Logica para manejar solo el primer error
            first_field_with_error = next(iter(err.messages))
            first_error_message = err.messages[first_field_with_error][0]
            
            # Otro error de validacion
            return jsonify({"error": "Datos invalidos", "message": first_error_message, "campo": first_field_with_error}), 422
        except Exception as e:
            self.logger.critical(f"Error validando la información: {e}")
            return jsonify({"error": "Error validando la información"}), 500
        finally:
            # Eliminar el directorio temporal
            self.logger.info("Función de validación finalizada")

    # Actualizar memorandos
    def vpnMemorando(self):
        try: 
            # Validacion de datos recibidos
            data = request.get_json()
            
            if not data:
                return jsonify({"error": "No se enviaron datos"}), 400
            
            # Preparacion de datos para validar
            datosProcesados = self.eliminar_campos_vacios(data)
            self.logger.info(f"Datos despues de limpieza: {datosProcesados}")

            # Validacion de los datos en schema
            self.form_schemaCampo.load(datosProcesados)
            self.logger.info("Ya se validaron correctamente")

            noformato = datosProcesados.get('numeroFormato')
            memorando = str(datosProcesados.get('memorando'))

            # Llamada al servicio de actualizacion de datos
            status_code = self.service.actualizar_memorando_vpn(memorando, noformato)

            # Epoch temporalmente aqui en lo que lo muevo a los servicios
            now = time.time()
            epoch = int(now)
            
            if status_code == 201:
                self.logger.info(f"Registro VPN Mayo actualizado con ID: {noformato} y memorando: {memorando}")
                # Enviar informacion al frontend
                return jsonify({"message": "Datos validados correctamente", "id": noformato, "epoch": epoch}), 200
            if status_code == 202:
                self.logger.info("No se logro actualizar el memorando")
                return jsonify({"error": "Datos incorrectos", "message": "No se logro actualizar el memorando"}), 401
            if status_code == 203:
                self.logger.error("No se encontró el Numero de Formato para editar")
                return jsonify({"error": "Datos incorrectos", "message": "No se encontró el número de formato para editar"}), 402
            if status_code == 400:
                self.logger.error("Ocurrio un error")
                return jsonify({"error": "Error interno", "message": "Ocurrio un error interno"}), 400
            else:
                self.logger.critical(f"Error interno actualizando memorando")
                # Enviar informacion al frontend
                return jsonify({"error": "Error interno actualizando memorando"}), 500

        except ValidationError as err:
            self.logger.error(f"Error de validación: {err.messages}")
            return jsonify({"error": "Datos inválidos", "message": err.messages}), 422
        except Exception as e:
            self.logger.critical(f"Error validando la información: {e}")
            return jsonify({"error": "Error validando la información"}), 500
        finally:
            self.logger.info("Función de validación finalizada")

    def telefonia(self):
        """
        Esta ruta es para validar todos los datos ingresados y resppnder rapidamente en caso de error,
        es mas ligera que la que genera el pdf.

        Args:
            data: Un diccionario.

        Returns:
            Token con id de la base de datos.
            Errores de validacion.
        """
        try:

            # Validacion de datos recibidos
            data = request.get_json()

            if not data:
                return jsonify({"error": "No se enviaron datos"}), 400
            
            # Preparacion de datos para validar
            datosProcesados = self.eliminar_campos_vacios(data)
            self.logger.info(f"Datos despues de limpieza: {datosProcesados}")

            # Validacion de los datos en schema
            self.forms_schemaTel.load(datosProcesados)
            self.logger.info("Ya se validaron correctamente")

            # Guardar en base de datos
            # Llamar al servicio y retornar el id
            tel_registro, status_code = self.service.add_Tel(datosProcesados)

            if status_code == 201:
                noformato = tel_registro.get('_id')
                epoch = tel_registro.get('epoch')
                self.logger.info(f"Registro Telefonia agregado con ID: {noformato}")

                # Enviar informacion al frontend
                return jsonify({"message": "Generando PDF", "id": noformato, "epoch": epoch}), 200
            else:
                self.logger.error(f"Error agregando el registro a la base de datos")
                # Enviar informacion al frontend
                return jsonify({"error": "Error agregando el registro a la base de datos"}), 500
            
        except ValidationError as err:
            # Logica para manejar solo el primer error
            first_field_with_error = next(iter(err.messages))
            first_error_message = err.messages[first_field_with_error][0]

            messages = err.messages
            self.logger.warning("Ocurrieron errores de validación")
            self.logger.info(f"Errores de validación completos: {messages}")
            
            # Otro error de validacion
            return jsonify({"error": "Datos invalidos", "message": first_error_message, "campo": first_field_with_error}), 422
        except Exception as e:
            self.logger.critical(f"Error validando la información: {e}")
            return jsonify({"error": "Error validando la información"}), 500
        finally:
            self.logger.info("Función de validación finalizada")

    def internet(self):
        """
        Esta ruta es para validar todos los datos ingresados y resppnder rapidamente en caso de error,
        es mas ligera que la que genera el pdf.

        Args:
            data: Un diccionario.

        Returns:
            Token con id de la base de datos.
            Errores de validacion.
        """
        try:

            # Validacion de datos recibidos
            data = request.get_json()

            if not data:
                return jsonify({"error": "No se enviaron datos"}), 400
            
            # Preparacion de datos para validar
            datosProcesados = self.eliminar_campos_vacios(data)
            self.logger.info(f"Datos despues de limpieza: {datosProcesados}")

            # Validacion de los datos en schema
            self.form_schemaInter.load(datosProcesados)
            self.logger.info("Ya se validaron correctamente")

            # Guardar en base de datos
            # Llamar al servicio y retornar el id
            inter_registro, status_code = self.service.add_Inter(datosProcesados)

            if status_code == 201:
                noformato = inter_registro.get('_id')
                epoch = inter_registro.get('epoch')
                self.logger.info(f"Registro Internet agregado con ID: {noformato}")

                # Enviar informacion al frontend
                return jsonify({"message": "Generando PDF", "id": noformato, "epoch": epoch}), 200
            else:
                self.logger.error(f"Error agregando el registro a la base de datos")
                # Enviar informacion al frontend
                return jsonify({"error": "Error agregando el registro a la base de datos"}), 500
            
        except ValidationError as err:
            # Logica para manejar solo el primer error
            first_field_with_error = next(iter(err.messages))
            first_error_message = err.messages[first_field_with_error][0]

            messages = err.messages
            self.logger.warning("Ocurrieron errores de validación")
            self.logger.info(f"Errores de validación completos: {messages}")
            
            # Otro error de validacion
            return jsonify({"error": "Datos invalidos", "message": first_error_message, "campo": first_field_with_error}), 422
        except Exception as e:
            self.logger.critical(f"Error validando la información: {e}")
            return jsonify({"error": "Error validando la información"}), 500
        finally:
            self.logger.info("Función de validación finalizada")

    def rfc(self):
        """
        Esta ruta es para validar todos los datos ingresados y resppnder rapidamente en caso de error,
        es mas ligera que la que genera el pdf.

        Args:
            data: Un diccionario.

        Returns:
            Token con id de la base de datos.
            Errores de validacion.
        """
        try:
            # Validacion de datos recibidos
            data = request.get_json()

            if not data:
                return jsonify({"error": "No se enviaron datos"}), 400
            
            # Preparacion de datos para validar
            datosProcesados = self.eliminar_campos_vacios(data)
            self.logger.info(f"Datos despues de limpieza: {datosProcesados}")

            # Validacion de los datos en schema
            self.forms_schemaRFC.load(datosProcesados)
            self.logger.info("Ya se validaron correctamente") 

            # Guardar en base de datos
            # Llamar al servicio y retornar el id
            rfc_registro, status_code = self.service.add_RFC(datosProcesados)

            if status_code == 201:
                noformato = rfc_registro.get('_id')
                epoch = rfc_registro.get('epoch')
                self.logger.info(f"Registro RFC agregado con ID: {noformato}")

                return jsonify({"message": "Generando PDF", "id": noformato, "epoch": epoch}), 200
            else:
                self.logger.error(f"Error agregando el registro a la base de datos")
                # Enviar informacion al frontend
                return jsonify({"error": "Error agregando el registro a la base de datos"}), 500
            
        except ValidationError as err:
            # Logica para manejar solo el primer error
            first_field_with_error = next(iter(err.messages))
            first_error_message = err.messages[first_field_with_error][0]

            messages = err.messages
            self.logger.warning("Ocurrieron errores de validación")
            self.logger.info(f"Errores de validación completos: {messages}")
            
            # Otro error de validacion
            return jsonify({"error": "Datos invalidos", "message": first_error_message, "campo": first_field_with_error}), 422
        except Exception as e:
            self.logger.critical(f"Error validando la información: {e}")
            return jsonify({"error": "Error validando la información"}), 500
        finally:
            self.logger.info("Función de validación finalizada")

        # Actualizar memorandos
    def rfcTicket(self):
        try: 
            # Validacion de datos recibidos
            data = request.get_json()
            
            if not data:
                return jsonify({"error": "No se enviaron datos"}), 400
            
            # Preparacion de datos para validar
            datosProcesados = self.eliminar_campos_vacios(data)
            self.logger.info(f"Datos despues de limpieza: {datosProcesados}")

            # Validacion de los datos en schema
            self.form_schemaCampo.load(datosProcesados)
            self.logger.info("Ya se validaron correctamente")

            noformato = datosProcesados.get('numeroFormato')
            ticket = str(datosProcesados.get('noticket'))

            # Llamada al servicio de actualizacion de datos
            status_code = self.service.actualizar_ticket_rfc(ticket, noformato)

            # Epoch temporalmente aqui en lo que lo muevo a los servicios
            now = time.time()
            epoch = int(now)
            
            if status_code == 201:
                self.logger.info(f"Registro VPN Mayo actualizado con ID: {noformato} y ticket: {ticket}")
                # Enviar informacion al frontend
                return jsonify({"message": "Datos validados correctamente", "id": noformato, "epoch": epoch}), 200
            if status_code == 202:
                self.logger.info("No se logro actualizar el ticket")
                return jsonify({"error": "Datos incorrectos", "message": "No se logro actualizar el ticket"}), 401
            if status_code == 203:
                self.logger.error("No se encontró el Numero de Formato para editar")
                return jsonify({"error": "Datos incorrectos", "message": "No se encontró el número de formato para editar"}), 402
            if status_code == 400:
                self.logger.error("Ocurrio un error")
                return jsonify({"error": "Error interno", "message": "Ocurrio un error interno"}), 400
            else:
                self.logger.critical(f"Error interno actualizando ticket")
                # Enviar informacion al frontend
                return jsonify({"error": "Error interno actualizando ticket"}), 500

        except ValidationError as err:
            self.logger.error(f"Error de validación: {err.messages}")
            return jsonify({"error": "Datos inválidos", "message": err.messages}), 422
        except Exception as e:
            self.logger.critical(f"Error validando la información: {e}")
            return jsonify({"error": "Error validando la información"}), 500
        finally:
            self.logger.info("Función de validación finalizada")

    # Busqueda
    def busquedaFolio(self):
        """
        Esta ruta es para validar todos los datos ingresados y resppnder rapidamente en caso de error,
        Es una busqueda por id de folio.

        Args:
            data: Un diccionario.

        Returns:
            Datos del registro con el id de folio proporcionado
        """
        try:
            # Validacion de datos recibidos
            data = request.get_json()

            if not data:
                return jsonify({"error": "No se enviaron datos"}), 400

            # Validacion de los datos en schema
            self.form_schemaFolio.load(data)
            self.logger.info("Ya se validaron correctamente") 

            # Guardar en base de datos
            # Llamar al servicio y retornar el id
            datosRegistro, status_code = self.service.obtener_datos_por_id('vpnMayo', data.get('id'))

            if status_code == 201:
                
                self.logger.info(f"Registro encontrado con id: {datosRegistro.get('_id')}")

                # if (datosRegistro.get('subgerencia', '') == "Subgerencia de Sistemas"): 
                return jsonify({"message": "Datos encontrados", "datos": datosRegistro}), 200
                # else:
                #     return jsonify({"error": "Número de formato no es de Subgerencia de Sistemas", "message": "Número de formato no accesible"}), 405
                    
            else:
                self.logger.error(f"No se encontró el registro a la base de datos, codigo: {status_code}")
                # Enviar informacion al frontend
                return jsonify({"error": "Datos incorrectos", "message": "No se encontró el número de formato"}), 402
            
        except ValidationError as err:
            # Logica para manejar solo el primer error
            first_field_with_error = next(iter(err.messages))
            first_error_message = err.messages[first_field_with_error][0]

            messages = err.messages
            self.logger.warning("Ocurrieron errores de validación")
            self.logger.info(f"Errores de validación completos: {messages}")
            
            # Otro error de validacion
            return jsonify({"error": "Datos invalidos", "message": first_error_message, "campo": first_field_with_error}), 422
        except Exception as e:
            self.logger.critical(f"Error validando la información: {e}")
            return jsonify({"error": "Error validando la información"}), 500
        finally:
            self.logger.info("Función de validación finalizada")

    # No sirve, solo es para conservar lo que teniamos antes
    def rfcFuncionORol(self):
        try: 
            # Recibimos datos
            data = request.get_json()

            # Validamos que existan datos
            if not data:
                return jsonify({"error": "Invalid data"}), 400
            
            # Validacion
            validated_data = self.actualizarFuncionRol.load(data)

            funcionrol = validated_data.get('funcionrol')
            nFormato = validated_data.get('numeroFormato')

            nRegistro = int(validated_data.get('numeroRegistro'))

            movimiento = validated_data.get('movimientoID')

            # Llamada al servicio de actualizacion de datos
            Datos, status_code = self.service.actualizar_funcionrol_rfc(nFormato, funcionrol, nRegistro, movimiento)

            if status_code == 201:
                self.logger.info("Información actualizada con exito en la base de datos")
                # Enviar archivo
                return self.rfc(Datos)
            if status_code == 202:
                self.logger.info("No se logro actualizar el FRO")
                return jsonify(Datos), status_code
            if status_code == 203:
                self.logger.error("No se encontró formato con  el ID especifico")
                return jsonify({"error": "No se encontró el ID de registro"}), status_code
            if status_code == 400:
                self.logger.error("Ocurrio un error")
                return jsonify({"error": "Error nuevo"}), status_code
            else:
                self.logger.error("Ocurrio otro error aqui")
                return jsonify({"error": "Error diferente"}), status_code

        except ValidationError as err:
            self.logger.error(f"Error de validación: {err.messages}")
            return jsonify({"error": "Datos inválidos", "details": err.messages}), 400
        except Exception as e:
            self.logger.error(f"Error generando PDF: {e}")
            return jsonify({"error": "Error generando PDF"}), 500

    def healthcheck(self):
        """Function to check the health of the services API inside the docker container"""
        return jsonify({"status": "Up"}), 200