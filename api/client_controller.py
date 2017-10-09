""" @package client_controller
"""
import json
from resource.shared_server import SharedServer
from model.client_shared import ClientShared
from model.car_shared import CarShared
from flask import jsonify

SHARED_SERVER = SharedServer()
CODIGO_OK = 0
TIPO_CLIENTE = "cliente"
TIPO_CHOFER = "chofer"

class ClientController:
    """Esta clase tiene los metodos para manajar la informacion de los clientes"""

    def __init__(self):
        """The constructor."""
        self.ref = ""

    def get_info_new_client(self, tipo):
        """ Este metodo solo sirve para las pruebas"""
        client = ClientShared.new_client(1, tipo, "Khaleesi", "Dragones3", "fb_user_id",
                                         "fb_auth_token", "Daenerys", "Targaryen", "Valyria",
                                         "madre_dragones@got.com", "01/01/1990")
        return client.get_json_new_client()

    def get_client(self, client_id):
        """ Este metodo devuelve la informacion del cliente buscado
            @param client_id es el id del cliente que se esta buscando la informacion"""
        informacion = SHARED_SERVER.get_client(client_id)
        response = jsonify(informacion)
        response.status_code = 200
        return response

    def get_clients(self, type_client):
        """ Este metodo devuelve la informacion de todos los cliente
            @param client_id es el id del cliente que se esta buscando la informacion"""
        response_shared_server = SHARED_SERVER.get_clients(type_client)
        if response_shared_server.status_code == 200:
            # Vamos a convertir nuestro json de clientes a uno con la info que corresponde
            # Hay que enviar response_shared_server.data y no el response
            response = self._convert_clients_json(response_shared_server)
            response.status_code = response_shared_server.status_code
        else:
            response = response_shared_server
        return response

    def post_new_client(self, client_json, type_client):
        """ Este metodo permite crear un cliente
            @param client informacion del cliente
            @param type_client tipo de cliente"""
        # Convertimos la info en el cliente y le ponemos el tipo
        client = ClientShared.new_client_json(client_json, type_client)
        # Mandamos la info al shared server
        response_shared_server = SHARED_SERVER.post_client(client)
        if response_shared_server.status_code == 201:
            #Esto lo hago asi porque el cuerpo del mensaje va a tener mucha info que no
            # necesita el cliente
            response = jsonify(
                mensaje="El cliente fue creado correctamente",
                codigo=CODIGO_OK,
            )
            response.status_code = response_shared_server.status_code
        else:
            response = response_shared_server
        return response

    def put_new_client(self, client_json, type_client, client_id):
        """ Este metodo permite modificar un cliente
            @param client informacion del cliente
            @param type_client tipo de cliente"""
        # Convertimos la info en el cliente y le ponemos el tipo
        client = ClientShared.new_client_json(client_json, type_client)
        # Mandamos la info al shared server
        response_shared_server = SHARED_SERVER.put_client(client_id, client)
        if response_shared_server.status_code == 201:
            #Esto lo hago asi porque el cuerpo del mensaje va a tener mucha info que no
            # necesita el cliente
            response = jsonify(
                mensaje="El cliente fue modificado correctamente",
                codigo=CODIGO_OK,
            )
            response.status_code = response_shared_server.status_code
        else:
            response = response_shared_server
        return response

    def delete_client(self, client_id):
        """ Este metodo permite eliminar un cliente
            @param client_id identificador del cliente"""
        response_shared_server = SHARED_SERVER.delete_client(client_id)
        json_data = json.loads(response_shared_server.text)
        response = jsonify(json_data)
        response.status_code = response_shared_server.status_code
        return response

    # Metodos para manipular la informacion de los autos

    def get_car(self, id_car, client_id):
        """ Este metodo devuelve la informacion del auto de un cliente
            @param id_car es el id del auto del cliente
            @param client_id es el id del cliente que se esta buscando la informacion"""
        informacion = SHARED_SERVER.get_car(id_car, client_id)
        if informacion.status_code == 200:
            #Filtro los datos que no le interesa al cliente
            car = json.loads(informacion.data)['car']
            response = jsonify(
                car_id=car.get('id'),
                owner=car.get('owner'),
                properties=car.get('properties')
            )
            response.status_code = 200
        else:
            # Si vino un error por el momento lo devuelvo, quizas hay que ver si conviene crear nuestros errores
            response = informacion
        return response

    def post_new_car(self, car_json, client_id):
        """ Este metodo permite crear un auto
            @param car_json informacion del auto
            @param client_id identificador del cliente"""
        # Convertimos la info en el cliente y le ponemos el tipo
        propertiesjson = jsonify(
            properties=car_json.get('properties')
        )
        # Mandamos la info al shared server
        response_shared_server = SHARED_SERVER.post_car(propertiesjson, client_id)
        if response_shared_server.status_code == 201:
            #Esto lo hago asi porque el cuerpo del mensaje va a tener mucha info que no
            # necesita el cliente
            response = jsonify(
                mensaje="El cliente fue creado correctamente",
                codigo=CODIGO_OK,
            )
            response.status_code = response_shared_server.status_code
        else:
            response = response_shared_server
        return response

    def put_new_car(self, car_json, car_id, driver_id):
        """ Este metodo permite modificar un cliente
            @param car_json informacion del auto
            @param car_id identificadore del auto
            @param driver_id identificador del conductor"""
        # Convertimos la info en el cliente y le ponemos el tipo
        propertiesjson = jsonify(
            properties=car_json.get('properties')
        )
        # Mandamos la info al shared server
        response_shared_server = SHARED_SERVER.put_car(propertiesjson, car_id, driver_id)
        if response_shared_server.status_code == 201:
            #Esto lo hago asi porque el cuerpo del mensaje va a tener mucha info que no
            # necesita el cliente
            response = jsonify(
                mensaje="El cliente fue modificado correctamente",
                codigo=CODIGO_OK,
            )
            response.status_code = response_shared_server.status_code
        else:
            response = response_shared_server
        return response

    def delete_car(self, driver_id, car_id):
        """ Este metodo permite eliminar un auto de un chofer
            @param car_id identificadore del auto
            @param driver_id identificador del conductor"""
        response_shared_server = SHARED_SERVER.delete_car(driver_id, car_id)
        #Devolvemos la respuesta que nos da el shared
        return response_shared_server

    ### Metodos privados ###

    def _convert_clients_json(self, json_clients):
        # Convertiremos el json que viene a nuestro propio json de clientes
        return json_clients
