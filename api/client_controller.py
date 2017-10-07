""" @package client_controller
"""
import json
from resource.shared_server import SharedServer
from model.client_shared import ClientShared
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
        response = jsonify(
            client_id=informacion.client_id,
            type_client=informacion.type_client,
            username=informacion.username,
            fb_user_id=informacion.fb_user_id,
            fb_auth_token=informacion.fb_auth_token,
            first_name=informacion.first_name,
            last_name=informacion.last_name,
            country=informacion.country,
            email=informacion.email,
            birthdate=informacion.birthdate
        )
        response.status_code = 200
        return response

    def get_driver(self, driver_id):
        """ Este metodo devuelve la informacion del chofer buscado
            @param driver_id es el id del chofer del que se esta buscando la informacion"""
        informacion = SHARED_SERVER.get_driver(driver_id)
        response = jsonify(
            client_id=informacion.client_id,
            type_client=informacion.type_client,
            username=informacion.username,
            fb_user_id=informacion.fb_user_id,
            fb_auth_token=informacion.fb_auth_token,
            first_name=informacion.first_name,
            last_name=informacion.last_name,
            country=informacion.country,
            email=informacion.email,
            birthdate=informacion.birthdate
        )
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
        #Devolvemos la respuesta que nos da el shared
        return response_shared_server

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

    ### Metodos privados ###

    def _convert_clients_json(self, json_clients):
        # Convertiremos el json que viene a nuestro propio json de clientes
        return json_clients
