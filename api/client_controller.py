""" @package client_controller
"""
import json
from resource.shared_server import SharedServer
from model.client_shared import ClientShared
from model.car_shared import CarShared
from flask import jsonify

SHARED_SERVER = SharedServer()
CODIGO_OK = 0
TIPO_CLIENTE = "passenger"
TIPO_CHOFER = "driver"

class ClientController:
    """Esta clase tiene los metodos para manajar la informacion de los clientes"""

    def __init__(self):
        """The constructor."""
        self.refs = {}

    def get_client(self, client_id):
        """ Este metodo devuelve la informacion del cliente buscado
            @param client_id es el id del cliente que se esta buscando la informacion"""
        response_shared_server = SHARED_SERVER.get_client(client_id)
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 200:
            client = json_data['user']
            self._save_ref(client_id, client.get('_ref'))
            response = jsonify(client)
        else:
            response = jsonify(json_data)
        response.status_code = response_shared_server.status_code
        return response

    def get_clients(self, type_client):
        """ Este metodo devuelve la informacion de todos los cliente
            @param client_id es el id del cliente que se esta buscando la informacion"""
        response_shared_server = SHARED_SERVER.get_clients()
        #Hay que filtrar los usuarios por tipos
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 200:
            clients = self._filter_user(json_data['users'], type_client)
            response = jsonify(clients)
        else:
            response = jsonify(json_data)
        response.status_code = response_shared_server.status_code
        return response

    def post_new_client(self, client_json, type_client):
        """ Este metodo permite crear un cliente
            @param client informacion del cliente
            @param type_client tipo de cliente"""
        # Le agregamos el tipo al cliente
        client_json['type'] = type_client

        # Mandamos la info al shared server
        response_shared_server = SHARED_SERVER.post_client(client_json)
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 201:
            client = json_data['user']
            self._save_ref(client.get('id'), client.get('_ref'))
            response = jsonify(client)
        else:
            response = jsonify(json_data)
        response.status_code = response_shared_server.status_code
        return response

    def put_new_client(self, client_json, type_client, client_id):
        """ Este metodo permite modificar un cliente
            @param client informacion del cliente
            @param type_client tipo de cliente"""
        # Le agregamos el tipo al cliente
        client_json['type'] = type_client
        client_json['_ref'] = self._get_ref_client(client_id)

        # Mandamos la info al shared server
        response_shared_server = SHARED_SERVER.put_client(client_id, client_json)
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 201:
            client = json_data['user']
            self._save_ref(client_id, client.get('_ref'))
            response = jsonify(client)
        else:
            response = jsonify(json_data)
        response.status_code = response_shared_server.status_code
        return response

    def delete_client(self, client_id):
        """ Este metodo permite eliminar un cliente
            @param client_id identificador del cliente"""
        response_shared_server = SHARED_SERVER.delete_client(client_id)
        json_data = ''
        if response_shared_server.text:
            json_data = json.loads(response_shared_server.text)
        response = jsonify(json_data)
        response.status_code = response_shared_server.status_code
        if response_shared_server.status_code == 204:
            self._delete_ref(client_id)
        return response

    # Metodos para manipular la informacion de los autos

    def get_car(self, id_car, client_id):
        """ Este metodo devuelve la informacion del auto de un cliente
            @param id_car es el id del auto del cliente
            @param client_id es el id del cliente que se esta buscando la informacion"""
        response_shared_server = SHARED_SERVER.get_car(id_car, client_id)
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 200:
            print(str(json_data))
            car = json_data['car']
            self._save_ref(self._key_car(client_id, id_car), car.get('_ref'))
            response = jsonify(car)
        else:
            response = jsonify(json_data)
        response.status_code = response_shared_server.status_code
        return response

    def post_new_car(self, car_json, client_id):
        """ Este metodo permite crear un auto
            @param car_json informacion del auto
            @param client_id identificador del cliente"""
        # Mandamos la info al shared server
        response_shared_server = SHARED_SERVER.post_car(car_json, client_id)
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 201:
            print(str(json_data))
            car = json_data['car']
            self._save_ref(self._key_car(client_id, car.get('id')), car.get('_ref'))
            response = jsonify(car)
        else:
            response = jsonify(json_data)
        response.status_code = response_shared_server.status_code
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

    def _get_ref_client(self, client_id):
        """ Este metodo devuelve el ref para manejar las colisiones de clientes
            @param client_id identificador del cliente"""
        ref = self.refs.get(client_id)
        if ref:
            return ref
        #Si no tenemos el ref lo buscamos
        response_shared_server = SHARED_SERVER.get_client(client_id)
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 200:
            data_client = json_data['user']
            self._save_ref(client_id, data_client.get('_ref'))
            return data_client.get('_ref')
        else:
            #Hubo un problema al buscar el get asi que no conseguimos el ref
            return ''

    def _save_ref(self, ref_id, ref):
        """ Este metodo guarda el ref para manejar las colisiones con el sharedServer
            @param ref_id identificador del objeto que maneja el sharedServer
            @param ref es el dato que necesita el sharedServer para identificar colisiones"""
        self.refs[ref_id] = ref

    def _delete_ref(self, ref_id):
        """ Este metodo elimina el ref
            @param ref_id identificador del objeto que maneja el sharedServer"""
        if self.refs.get(ref_id):
            self.refs.pop(ref_id)

    def _key_car(self, client_id, id_car):
        """ Devuelve la key de un auto para manejar los colisiones
        """
        return str(client_id) + '&' + str(id_car)

    def _filter_user(self, users, type_client):
        """ Este metodo filtra los usuarios segun su tipo
            @param type_client tipo de clientes que se espera obtener
            @param users es la informacion de todos los usuarios"""
        clients = []
        for user in users:
            if user.get('type') == type_client:
                clients.append(user)
        return clients
