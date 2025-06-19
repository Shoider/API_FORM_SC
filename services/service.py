import datetime
import time
from flask import jsonify
from pymongo import ReturnDocument
from logger.logger import Logger
from bson.errors import InvalidId

class Service:
    """Service class to that implements the logic of the CRUD operations for tickets"""

    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn
        
    def add_VPNMayo(self, new_vpn):
        """
        Función para añadir un registro de VPN Mayo a la base de datos.
        Utiliza el método genérico para la creación de ID e inserción.
        """
        # Llamamos a nuestra función genérica con los parámetros específicos para VPN Mayo.
        return self._add_document_with_custom_id(
            document_data=new_vpn,
            data_collection_name="vpnMayo",
            counter_collection_name="vpnMayoCounters",
            document_type_name="VPN Mayo"
        )
        
    def add_Tel(self, new_tel):
        """
        Función para añadir un registro de Telefonia a la base de datos.
        Utiliza el método genérico para la creación de ID e inserción.
        """
        # Llamamos a nuestra función genérica con los parámetros específicos para Telefonia.
        return self._add_document_with_custom_id(
            document_data=new_tel,
            data_collection_name="tel",
            counter_collection_name="telCounters",
            document_type_name="Telefonia"
        )
    
    def add_Inter(self, new_inter):
        """
        Función para añadir un registro de Internet a la base de datos.
        Utiliza el método genérico para la creación de ID e inserción.
        """
        # Llamamos a nuestra función genérica con los parámetros específicos para Internet.
        return self._add_document_with_custom_id(
            document_data=new_inter,
            data_collection_name="internet",
            counter_collection_name="internetCounters",
            document_type_name="Internet"
        )
    
    def add_RFC(self, new_rfc):
        """
        Función para añadir un registro de RFC a la base de datos.
        Utiliza el método genérico para la creación de ID e inserción.
        """
        # Llamamos a nuestra función genérica con los parámetros específicos para Telefonia.
        return self._add_document_with_custom_id(
            document_data=new_rfc,
            data_collection_name="rfc",
            counter_collection_name="rfcCounters",
            document_type_name="RFC"
        )
    
    # Aqui van actualizaciones de memorandos o tickets

    def actualizar_memorando_vpn(self, nuevo_memorando, documento_id):
        """
        Busca un documento en MongoDB por su ID, actualiza el campo 'memorando'
        y retorna el documento original antes de la actualización.

        Args:
            documento_id (str): El ID del documento a actualizar.
            nuevo_memorando (str): El nuevo valor para el campo 'memorando'.
        """
        try:
            vpn_collection = self.db_conn.db['vpnMayo']
            # Buscar el documento por su ID
            documento_original = vpn_collection.find_one({'_id': documento_id})

            if documento_original:
                # Actualizar el campo 'memorando'
                resultado = vpn_collection.update_one(
                    {'_id': documento_id},
                    {'$set': {'memorando': nuevo_memorando}}
                )

                if resultado.modified_count > 0:
                    return 201
                else:
                    # Si no se modificó nada (aunque se encontró el documento),
                    # podría ser un caso a considerar en tu lógica de manejo de errores.
                    return 202
            else:
                return 203 # No se encontró el documento con el ID proporcionado
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 400
        
    def actualizar_ticket_rfc(self, nuevo_ticket, documento_id):
        """
        Busca un documento en MongoDB por su ID, actualiza el campo 'noticket'
        y retorna el documento original antes de la actualización.

        Args:
            documento_id (str): El ID del documento a actualizar.
            nuevo_memorando (str): El nuevo valor para el campo 'memorando'.
        """
        try:
            rfc_collection = self.db_conn.db['rfc']
            # Buscar el documento por su ID
            documento_original = rfc_collection.find_one({'_id': documento_id})

            if documento_original:
                # Actualizar el campo 'memorando'
                resultado = rfc_collection.update_one(
                    {'_id': documento_id},
                    {'$set': {'memorando': nuevo_ticket}}
                )

                if resultado.modified_count > 0:
                    return 201
                else:
                    # Si no se modificó nada (aunque se encontró el documento),
                    # podría ser un caso a considerar en tu lógica de manejo de errores.
                    return 202
            else:
                return 203 # No se encontró el documento con el ID proporcionado
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 400
        
    # No sirve, solo es para conservar lo que teniamos antes 
    def actualizar_funcionrol_rfc(self, documento_id, nuevo_funcionrol, id_registro, tabla) -> dict:

        try:
            rfc_collection = self.db_conn.db['rfc']
            # Buscar el documento por su ID
            documento_original = rfc_collection.find_one({'_id': documento_id})

            if not documento_original:
                return jsonify({"error": "No se encontró el documento con el ID proporcionado"}), 203

            # Para cambios
            registrosAltas = len(documento_original['registrosInterAltas'])
            registrosBajas = len(documento_original['registrosInterBajas'])

            if (tabla == "ALTAS" and registrosAltas >= id_registro):
                resultado = rfc_collection.update_one(
                    {'_id': documento_id},
                    {'$set': {'registrosInterAltas.$[elem].FRO': nuevo_funcionrol}},
                    array_filters=[{'elem.id': id_registro}]
                )
            elif (tabla == "ALTAS" and registrosAltas < id_registro):
                id_registro = id_registro - registrosAltas
                resultado = rfc_collection.update_one(
                    {'_id': documento_id},
                    {'$set': {'registrosInterCambiosAltas.$[elem].FRO': nuevo_funcionrol}},
                    array_filters=[{'elem.id': id_registro}]
                )
            elif (tabla == "BAJAS" and registrosBajas >= id_registro):
                resultado = rfc_collection.update_one(
                    {'_id': documento_id},
                    {'$set': {'registrosInterBajas.$[elem].FRO': nuevo_funcionrol}},
                    array_filters=[{'elem.id': id_registro}]
                )
            elif (tabla == "BAJAS" and registrosBajas < id_registro):
                id_registro = id_registro - registrosBajas
                resultado = rfc_collection.update_one(
                    {'_id': documento_id},
                    {'$set': {'registrosInterCambiosBajas.$[elem].FRO': nuevo_funcionrol}},
                    array_filters=[{'elem.id': id_registro}]
                )
            else:
                return None, 400
            
            documento_nuevo = rfc_collection.find_one({'_id': documento_id})

            if resultado.modified_count > 0:
                self.logger.info(f"Documento con _id '{documento_id}' actualizado exitosamente.")
                return documento_nuevo, 201
            else:
                self.logger.info(
                    f"No se encontró el subdocumento con id '{id_registro}' "
                    f"en 'registrosInter{tabla}' para el documento con _id '{documento_id}', "
                    f"o el valor de FRO ya era el mismo."
                )
                return documento_nuevo, 202

        except Exception as e:
            self.logger.info(f"Ocurrió un error: {e}")
            return None, 400
        
    
    # Funciones genericas reutilizables:

    def _add_document_with_custom_id(self, document_data, data_collection_name, counter_collection_name, document_type_name):
        """
        Función genérica para añadir un documento a la base de datos con un ID personalizado.
        El ID se genera usando la fecha actual (YYMMDD) y un contador diario atómico.

        :param document_data: (dict) El diccionario de datos a insertar.
        :param data_collection_name: (str) El nombre de la colección donde se insertará el documento.
        :param counter_collection_name: (str) El nombre de la colección para el contador diario.
        :param document_type_name: (str) Un nombre descriptivo para el tipo de documento (para logs/errores).
        :return: Una tupla con un diccionario de respuesta y el código de estado HTTP.
        """
        try:
            # Obtenemos la fecha y hora actual para construir el ID.
            now = datetime.datetime.now()
            yy = now.strftime("%y")
            mm = now.strftime("%m")
            dd = now.strftime("%d")
            base_id = f"{yy}{mm}{dd}"

            # Usamos find_one_and_update para asegurar que la operación sea atómica.
            # Esto evita que dos peticiones obtengan el mismo número de secuencia al mismo tiempo.
            # `upsert=True` crea el contador del día si no existe.
            counter_doc = self.db_conn.db[counter_collection_name].find_one_and_update(
                {"_id": base_id},
                {"$inc": {"seq": 1}},
                upsert=True,
                return_document=ReturnDocument.AFTER,
            )

            sequence = counter_doc.get("seq", 1)
            padded_sequence = str(sequence).zfill(4)
            custom_id = f"{base_id}{padded_sequence}"

            # Añadimos el ID generado y la fecha de generación al documento.
            document_data["_id"] = custom_id
            document_data["fecha"] = now.strftime("%d-%m-%Y")  # Formato: DD-MM-YYYY

            # Epoch
            now = time.time()
            epoch = int(now)
            document_data["epoch"] = epoch

            # Insertamos el documento en la colección de datos correspondiente.
            # Usamos corchetes `[]` para acceder a la colección a través de una variable.
            self.db_conn.db[data_collection_name].insert_one(document_data)

            # Si todo sale bien, devolvemos el ID, epoch y el código 201 (Creado).
            return {"_id": custom_id, "epoch": epoch}, 201

        except Exception as e:
            # Si algo falla, lo registramos en el log y devolvemos un error 500.
            error_message = f"Error adding {document_type_name} register to database with custom ID: {e}"
            self.logger.error(error_message)
            return jsonify({"error": error_message}), 500
        
    def obtener_datos_por_id(self, collection_name: str, document_id: str) -> dict:
        """
        Busca y devuelve un único documento de una colección por su _id.

        Args:
            collection_name (str): El nombre de la colección donde buscar.
            document_id (str): El ID del documento en formato de texto (string).

        Returns:
            dict: El documento encontrado.
            None: Si el documento no se encuentra o el ID es inválido.
        """
        try:
            # Obtener la colección desde la base de datos
            collection = self.db_conn.db[collection_name]
            
            # --- El paso más importante: Convertir el string a ObjectId ---
            datos = collection.find_one({'_id': document_id})
            #object_id_to_find = ObjectId(document_id)
            
            # --- La consulta: Usar find_one para obtener un solo documento ---
            # find_one() es más eficiente que find() si solo esperas un resultado.
            #document = collection.find_one({"_id": object_id_to_find})
            
            # Regresamos el diccionario de datos 
            return datos, 201

        except InvalidId:
            # Esto ocurre si el string del document_id no tiene un formato válido
            # (ej. es muy corto, muy largo o tiene caracteres inválidos).
            print(f"Error: El ID '{document_id}' no es un ObjectId válido.")
            return None, 400
            
        except Exception as e:
            # Manejar otros posibles errores (ej. de conexión)
            print(f"Ocurrió un error inesperado: {e}")
            return None, 500