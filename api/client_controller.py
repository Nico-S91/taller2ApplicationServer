""" @package api.client_controller
"""
import json
from service.shared_server import SharedServer
from service.shared_server import TIPO_CHOFER
from api.trip_controller import TripController
from api.model_manager import ModelManager
from flask import jsonify
from api.trip_controller import _get_response_not_exist_user
from api.trip_controller import _get_response_not_driver
from api.trip_controller import CODE_ERROR
from api.trip_controller import CODE_OK

SHARED_SERVER = SharedServer()
TRIP_CONTROLLER = TripController()
MODEL_MANAGER = ModelManager()
CODIGO_OK = 0
CAMPO_COLISIONES = '_ref'
JSON_CAR = 'car'
JSON_CLIENT = 'user'

class ClientController:
    """Esta clase tiene los metodos para manajar la informacion de los clientes"""

    def __init__(self):
        """The constructor."""
        self.client_refs = {}
        self.car_refs = {}

    def get_client(self, client_id):
        """ Este metodo devuelve la informacion del cliente buscado
            @param client_id identificado del cliente"""
        response_shared_server = SHARED_SERVER.get_client(client_id)
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 200:
            client = json_data[JSON_CLIENT]
            self._save_ref(client_id, client.get(CAMPO_COLISIONES))
            self._add_user_mongo(client_id, client)
            response = jsonify(client)
        else:
            response = jsonify(json_data)
        response.status_code = response_shared_server.status_code
        return response

    def get_clients(self, type_client):
        """ Este metodo devuelve la informacion de todos los cliente de un tipo
            @param type_client tipo de cliente buscado"""
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
            client = json_data[JSON_CLIENT]
            client_id = client.get('id')
            self._save_ref(client_id, client.get(CAMPO_COLISIONES))
            self._add_user_mongo(client_id, client)
            response = jsonify(client)
        else:
            response = jsonify(json_data)
        response.status_code = response_shared_server.status_code
        return response

    def put_new_client(self, client_json, type_client, client_id):
        """ Este metodo permite modificar un cliente
            @param client informacion del cliente
            @param type_client tipo de cliente
            @param client_id identificado del cliente"""
        # Le agregamos el tipo al cliente
        client_json['type'] = type_client
        client_json[CAMPO_COLISIONES] = self._get_ref_client(client_id)

        # Mandamos la info al shared server
        response_shared_server = SHARED_SERVER.put_client(client_id, client_json)
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 201:
            client = json_data[JSON_CLIENT]
            self._save_ref(client_id, client.get(CAMPO_COLISIONES))
            self._update_client_mongo(client_id, client)
            response = jsonify(client)
        else:
            response = jsonify(json_data)
        response.status_code = response_shared_server.status_code
        return response

    def put_client_available(self, client_id, available):
        """ Este metodo modifica la disponibilidad de un cliente
            @param client_id identificador del cliente
            @param available es un boolean que indica si esta o no disponible"""
        #Primero debo ver que exista el cliente, en la base nuestra
        info_client = MODEL_MANAGER.get_info_usuario(client_id)
        type_client = None
        if info_client is None:
            #Buscamos en el shared server
            response_shared_server = SHARED_SERVER.get_client(client_id)
            json_data = json.loads(response_shared_server.text)
            if response_shared_server.status_code == 200:
                client = json_data[JSON_CLIENT]
                self._save_ref(client_id, client.get(CAMPO_COLISIONES))
                self._add_user_mongo(client_id, client)
                type_client = client.get('type')
            else:
                return _get_response_not_exist_user(client_id)
        else:
            type_client = info_client.get('client_type')

        if type_client is None or type_client != TIPO_CHOFER:
            return _get_response_not_driver(client_id)
        result = MODEL_MANAGER.change_available_driver(client_id, available)
        if result:
            if available:
                message = 'El chofer ' + str(client_id) + ' ya se encuentra disponible.'
            else:
                message = 'El chofer ' + str(client_id) + ' ya no se encuentra disponible.'
            response = jsonify(code=CODE_OK, message=message)
            response.status_code = 201
            return response
        else:
            response = jsonify(code=CODE_OK, message='No se pudo modificar la disponibilidad' +
                               ' del chofer ' + str(client_id) + ', vuelva a intentarlo mas tarde.')
            response.status_code = 400
            return response

    def delete_client(self, client_id):
        """ Este metodo permite eliminar un cliente
            @param client_id identificador del cliente"""
        response_shared_server = SHARED_SERVER.delete_client(client_id)
        json_data = ''
        if response_shared_server.text:
            json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 204:
            self._delete_ref(client_id)
            MODEL_MANAGER.delete_usuario(client_id)
            json_data = json.loads("""{
                    "mensaje": "Se elimino correctamente el usuario"
                }""")
        response = jsonify(json_data)
        response.status_code = response_shared_server.status_code
        return response

    def get_closest_clients(self, type_client, lat, lon, ratio):
        """ Este metodo devuelve los clientes que esten cercanos a una determinada posicion
            @param type_client es el tipo de cliente
            @param lat es la latitud del lugar donde se busca
            @param lon es la longitud del lugar donde se busca
            @param ratio es el radio que se busca a los clientes"""
        #Primero busco las ubicaciones de los choferes
        locations = TRIP_CONTROLLER.get_closest_clients(type_client, lat, lon, ratio)
        clients = []
        if locations == []:
            print('Esta vacio')
            return jsonify(clients)
        for location in locations:
            id_client = location.get('user_id')
            #Veo si el cliente esta disponible
            is_available = MODEL_MANAGER.user_is_available(id_client)
            if is_available is not None and is_available:
                trips = MODEL_MANAGER.get_started_and_unfinished_trips_with_driver_id(id_client)
                if trips is None or trips == []:
                    response_client = self.get_client(id_client)
                    if response_client.status_code == 200:
                        json_data = {
                            'info' : json.loads(response_client.data),
                            'location' : location
                        }
                        clients.append(json_data)
        return jsonify(clients)

    # Metodos para manipular la informacion de los autos

    def get_car(self, car_id, driver_id):
        """ Este metodo devuelve la informacion del auto de un cliente
            @param car_id identificado del auto del cliente
            @param driver_id identificado del chofer"""
        response_shared_server = SHARED_SERVER.get_car(car_id, driver_id)
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 200:
            car = json_data[JSON_CAR]
            self._save_car_ref(driver_id, car_id, car.get(CAMPO_COLISIONES))
            response = jsonify(car)
        else:
            response = jsonify(json_data)
        response.status_code = response_shared_server.status_code
        return response

    def get_cars(self, driver_id):
        """ Este metodo devuelve la informacion de los autos de un cliente
            @param driver_id identificado del chofer"""
        response_shared_server = SHARED_SERVER.get_cars(driver_id)
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 200:
            cars = json_data['cars']
            response = jsonify(cars)
        else:
            response = jsonify(json_data)
        response.status_code = response_shared_server.status_code
        return response

    def post_new_car(self, car_json, driver_id):
        """ Este metodo permite crear un auto
            @param car_json informacion del auto
            @param driver_id identificador del chofer"""
        response_shared_server = SHARED_SERVER.post_car(car_json, driver_id)
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 200:
            car = json_data[JSON_CAR]
            self._save_car_ref(driver_id, car.get('id'), car.get(CAMPO_COLISIONES))
            response = jsonify(car)
        else:
            response = jsonify(json_data)
        response.status_code = response_shared_server.status_code
        return response

    def put_new_car(self, car_json, car_id, driver_id):
        """ Este metodo permite modificar un auto
            @param car_json informacion del auto
            @param car_id identificadore del auto
            @param driver_id identificador del chofer"""
        #Le agregamos el campo de las colisiones para que todo funciones
        car_json[CAMPO_COLISIONES] = self._get_ref_car(driver_id, car_id)

        response_shared_server = SHARED_SERVER.put_car(car_json, car_id, driver_id)
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 201:
            car = json_data[JSON_CAR]
            self._save_car_ref(driver_id, car_id, car.get(CAMPO_COLISIONES))
            response = jsonify(car)
        else:
            response = jsonify(json_data)
        response.status_code = response_shared_server.status_code
        return response

    def delete_car(self, driver_id, car_id):
        """ Este metodo permite eliminar un auto de un chofer
            @param car_id identificadore del auto
            @param driver_id identificador del chofer"""
        response_shared_server = SHARED_SERVER.delete_car(driver_id, car_id)
        json_data = ''
        if response_shared_server.text:
            json_data = json.loads(response_shared_server.text)
        response = jsonify(json_data)
        response.status_code = response_shared_server.status_code
        if response_shared_server.status_code == 204:
            self._delete_car_ref(driver_id, car_id)
        return response

    ### Metodos privados ###

    def _get_ref_client(self, client_id):
        """ Este metodo devuelve el ref para manejar las colisiones de clientes
            @param client_id identificador del cliente"""
        ref = self.client_refs.get(client_id)
        if ref:
            return ref
        #Si no tenemos el ref lo buscamos
        response_shared_server = SHARED_SERVER.get_client(client_id)
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 200:
            data_client = json_data[JSON_CLIENT]
            self._save_ref(client_id, data_client.get(CAMPO_COLISIONES))
            return data_client.get(CAMPO_COLISIONES)
        else:
            #Hubo un problema al buscar el get asi que no conseguimos el ref
            return ''

    def _save_ref(self, ref_id, ref):
        """ Este metodo guarda el ref para manejar las colisiones con el sharedServer
            @param ref_id identificador del objeto que maneja el sharedServer
            @param ref es el dato que necesita el sharedServer para identificar colisiones"""
        self.client_refs[ref_id] = ref

    def _delete_ref(self, ref_id):
        """ Este metodo elimina el ref
            @param ref_id identificador del objeto que maneja el sharedServer"""
        if self.client_refs.get(ref_id):
            self.client_refs.pop(ref_id)

    def _key_car(self, client_id, id_car):
        """ Devuelve la key de un auto para manejar los colisiones
        """
        return str(client_id) + '&' + str(id_car)

    def _get_ref_car(self, client_id, car_id):
        """ Este metodo devuelve el ref para manejar las colisiones de clientes
            @param client_id identificador del cliente
            @param car_id identificador del auto"""
        key = self._key_car(client_id, car_id)
        ref = self.car_refs.get(key)
        if ref:
            return ref
        #Si no tenemos el ref lo buscamos
        response_shared_server = SHARED_SERVER.get_car(client_id, car_id)
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 200:
            data_car = json_data[JSON_CAR]
            self._save_car_ref(client_id, car_id, data_car.get(CAMPO_COLISIONES))
            return data_car.get(CAMPO_COLISIONES)
        else:
            #Hubo un problema al buscar el get asi que no conseguimos el ref
            return ''

    def _save_car_ref(self, driver_id, car_id, ref):
        """ Este metodo guarda el ref del auto para manejar las colisiones con el sharedServer
            @param driver_id identificador del chofer
            @param car_id identificador del auto
            @param ref es el dato que necesita el sharedServer para identificar colisiones"""
        key = self._key_car(driver_id, car_id)
        self.car_refs[key] = ref

    def _delete_car_ref(self, driver_id, car_id):
        """ Este metodo elimina el ref del auto
           @param driver_id identificador del chofer
            @param car_id identificador del auto"""
        key = self._key_car(driver_id, car_id)
        if self.car_refs.get(key):
            self.car_refs.pop(key)

    def _filter_user(self, users, type_client):
        """ Este metodo filtra los usuarios segun su tipo
            @param users es la informacion de todos los usuarios
            @param type_client tipo de clientes que se espera obtener"""
        clients = []
        for user in users:
            if user.get('type') == type_client:
                clients.append(user)
        return clients

    def _add_user_mongo(self, user_id, user):
        """ Este metodo agrega la informacion de un usuario a nuestra base de datosS
            @param user_id es el identificador del usuario
            @param user es la informacion del usuario"""
        if MODEL_MANAGER.get_info_usuario(user_id) is None:
            MODEL_MANAGER.add_usuario(user_id, user.get('type'), user.get('username'), True)

    def _update_client_mongo(self, user_id, user):
        """ Este metodo modifica la informacion de un usuario en nuestra base de datos
            @param user_id es el identificador del usuario
            @param user es la informacion del usuario"""
        if MODEL_MANAGER.get_info_usuario(user_id) is None:
            MODEL_MANAGER.add_usuario(user_id, user.get('type'), user.get('username'), True)
        else:
            MODEL_MANAGER.update_usuario(user_id, user.get('type'), user.get('username'), True)
