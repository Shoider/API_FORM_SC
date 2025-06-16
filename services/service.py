import datetime
import time
from flask import jsonify
from pymongo import ReturnDocument
from logger.logger import Logger

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
    
    # Aqui van actualizaciones de memorandos

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