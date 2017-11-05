""" @package api.trip_controller
"""
import json
from flask import jsonify
from model import db_manager
from service.shared_server import SharedServer
from service.shared_server import TIPO_CLIENTE
from service.shared_server import TIPO_CHOFER
from api.model_manager import ModelManager

SHARED_SERVER = SharedServer()
MODEL_MANAGER = ModelManager()

class TripController:
    """Esta clase tiene los metodos para manajar la informacion de los viajes"""

    def __init__(self):
        """The constructor."""
        self.refs = {}

    def get_trip(self, type_user, user_id, trip_id):
        """ Este metodo devuelve la informacion de un viaje
            @param type_user es el tipo de usuario del viaje
            @param user_id es el identificador del usuario
            @param trip_id es el identificador del viaje"""
        response_shared_server = SHARED_SERVER.get_trip(trip_id)
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 200:
            json_response = json_data['trip']
            # Si el viaje no pertenece al usuario entonces no le podemos pasar la informacion
            if not self._is_your_trip(type_user, user_id, json_response):
                return self._get_response_trip_unauthorized()
        else:
            json_response = json_data
        response = jsonify(json_response)
        response.status_code = response_shared_server.status_code
        return response

    def get_trips(self, user_id):
        """ Este metodo devuelve la informacion de todos los viaje de un usuario
            @param type_user es el tipo de usuario del viaje
            @param user_id es el identificador del usuario"""
        response_shared_server = SHARED_SERVER.get_trips(user_id)
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 200:
            json_response = json_data['trips']
        else:
            json_response = json_data
        response = jsonify(json_response)
        response.status_code = response_shared_server.status_code
        return response

    def accept_trip(self, driver_id, trip_id):
        """ Este metodo al conductor aceptar un viaje
            @param driver_id identificador del cliente
            @param trip_id identificador del viaje"""
        #Vamos a verificar que el driver_id es un chofer
            #sino tirar excepcion "El usuario no es un chofer"

        #Vamos a verificar que el conductor puede aceptar ese viaje
        #si el driver_id es el mismo que el que guarda el viaje
            #entonce se acepta el viaje
        #si esta vacio el identificador en el viaje
            #entonces se le agrega el identificador al viaje y se acepta
        #sino tirar excepcion "El viaje ya esta asignado a otro chofer"


    def post_new_estimate(self, data):
        """ Este metodo permite devuelve la estimacion de un viaje
            @param car_json informacion del auto
            @param driver_id identificador del cliente"""
        response_shared_server = SHARED_SERVER.post_trip_estimate(data)
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 201:
            json_data = json_data['cost']
        response = jsonify(json_data)
        response.status_code = response_shared_server.status_code
        return response

    def get_last_location(self, user_id):
        """ Devuelve response de ultima ubicacion
            @param user_id un id de usuario
        """
        response = MODEL_MANAGER.get_last_known_position(user_id)
        response.status_code = 200
        return response

    def post_new_last_location(self, data):
        """ guarda la nueva ultima ubicacion de un usuario
            si no habia una anterior, la crea, sino la modifica
            @param data el json de request para dar de alta la ubicacion
        """
        user_id = data.get('user_id')
        user_type = data.get('user_type')
        lat = data.get('lat')
        lon = data.get('long')
        operation_result = MODEL_MANAGER.add_last_known_position(user_id, user_type, lat, lon)
        response = jsonify({
            'operation_result': operation_result
        })
        response.status_code = 200
        return response

    def get_closest_clients(self, type_client, lat, lon, radio):
        """ Este metodo devuelve los ids de los clientes que se encontraron en el radio de busqueda
            @param type_user es el tipo de usuario del viaje
            @param lat es la latitud de la ubicacion
            @param lon es la longitud de la ubicacion
            @param radio es el radio de busqueda"""
        #Calculo la latitud de busqueda
        min_lat = lat - radio
        max_lat = lat + radio
        #Calculo la latitud de busqueda
        min_lon = lon - radio
        max_lon = lon + radio
        #Busco las ubicaciones de todos los clientes que son del tipo type_client
        clients = db_manager.get_locations_by_type(type_client)
        if clients == []:
            return []
        #Filtro los clientes que cumplen con la latitud y longitud buscada
        ids = []
        for client in clients:
            lat_client = float(client.get("lat"))
            lon_client = float(client.get("long"))
            if min_lat <= lat_client <= max_lat:
                if min_lon <= lon_client <= max_lon:
                    ids.append(client.get("id"))
        return ids

    #Metodos privados

    def _is_your_trip(self, type_user, user_id, json_response):
        """ Este metodo devuelve la informacion de un viaje
            @param type_user es el tipo de usuario del viaje
            @param user_id es el identificador del usuario
            @param json_response es la informacion del viaje"""
        if type_user == TIPO_CHOFER or type_user == TIPO_CLIENTE:
            if json_response[type_user] == user_id:
                return True
        return False

    def _get_response_trip_unauthorized(self):
        """ Devuelve el response que indica que el viaje no pertenece al usuario"""
        response = jsonify({
            'code': -1,
            'message': 'El viaje no pertenece al usuario'
        })
        response.status_code = 401
        return response
