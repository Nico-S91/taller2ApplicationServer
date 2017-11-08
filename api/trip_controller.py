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
        """ Este metodo permite al conductor aceptar un viaje
            @param driver_id identificador del chofer
            @param trip_id identificador del viaje"""
        is_driver = True
        info_user = MODEL_MANAGER.get_info_usuario(driver_id)
        #Verificamos que el usuario sea un chofer
        if info_user == {}:
            response_shared_server = SHARED_SERVER.get_client(driver_id)
            if response_shared_server.status_code != 200:
                #VER QUE OTROS ERRORES PUEDE DEVOLVER EL SHARED SERVER!!!
                #No existe el usuario
                response = jsonify(code=-5, message='El usuario ' + str(driver_id) + ' no existe.')
                response.status_code = 404
                return response
            else:
                info_user = json.loads(response_shared_server.text).get('user')
                if info_user.get('type') != TIPO_CHOFER:
                    is_driver = False
                #Agrego la info a la base
                MODEL_MANAGER.add_usuario(driver_id, info_user.get('type'),
                                          info_user.get('username'))
        else:
            if info_user.get('typeClient') != TIPO_CHOFER:
                is_driver = False
        if is_driver is False:
            response = jsonify(code=-2, message='El usuario ' + str(driver_id) +
                               ' no es un chofer.')
            response.status_code = 400
            return response

        #Vamos a verificar que el conductor puede aceptar ese viaje
        response_mongo = False
        info_trip = MODEL_MANAGER.get_trip(trip_id)
        if info_trip is None:
            response = jsonify(code=-4, message='El viaje ' + str(trip_id) + ' no existe.')
            response.status_code = 404
            return response
        if info_trip.get('driver_id') is None:
            #Agrego el identificador al viaje y se acepto
            response_mongo = MODEL_MANAGER.add_driver_to_trip(trip_id, driver_id)
            if response_mongo:
                response_mongo = MODEL_MANAGER.accept_trip(trip_id)
        else:
            if info_trip.get('driver_id') == driver_id:
                #Acepto el viaje
                response_mongo = MODEL_MANAGER.accept_trip(trip_id)
            else:
                response = jsonify(code=-3, message='El viaje ' + str(trip_id) +
                                   ' esta asignado a otro chofer.')
                response.status_code = 400
                return response
        if response_mongo:
            #Se pudo aceptar el viaje
            response = jsonify(code=0, message='El chofer ' + str(driver_id) +
                               ' acepto el viaje ' + str(trip_id) + '.')
            response.status_code = 201
            return response
        else:
            response = jsonify(code=-1, message='El chofer ' + str(driver_id) +
                               ' no pudo aceptar el viaje ' + str(trip_id) +
                               ', vuelva a intentarlo mas tarde.')
            response.status_code = 400
            return response

    def start_trip(self, client_id, trip_id):
        """ Este metodo indica que se comenzo un viaje
            @param client_id identificador del cliente
            @param trip_id identificador del viaje"""
        is_client = True
        info_user = MODEL_MANAGER.get_info_usuario(client_id)
        #Verificamos que el usuario sea un cliente
        if info_user == {}:
            response_shared_server = SHARED_SERVER.get_client(client_id)
            if response_shared_server.status_code != 200:
                #VER QUE OTROS ERRORES PUEDE DEVOLVER EL SHARED SERVER!!!
                #No existe el usuario
                response = jsonify(code=-5, message='El usuario ' + str(client_id) + ' no existe.')
                response.status_code = 404
                return response
            else:
                info_user = json.loads(response_shared_server.text).get('user')
                if info_user.get('type') != TIPO_CLIENTE:
                    is_client = False
                #Agrego la info a la base
                MODEL_MANAGER.add_usuario(client_id, info_user.get('type'),
                                          info_user.get('username'))
        else:
            if info_user.get('typeClient') != TIPO_CLIENTE:
                is_client = False
        if is_client is False:
            response = jsonify(code=-2, message='El usuario ' + str(client_id) +
                               ' no es un pasajero.')
            response.status_code = 400
            return response

        #Vamos a verificar que el viaje pertenezca al cliente
        response_mongo = False
        info_trip = MODEL_MANAGER.get_trip(trip_id)
        if info_trip is None:
            response = jsonify(code=-4, message='El viaje ' + str(trip_id) + ' no existe.')
            response.status_code = 404
            return response
        if info_trip.get('passenger_id') is None:
            response = jsonify(code=-7, message='El viaje ' + str(trip_id) +
                               ' no le pertenece al usuario ' + client_id + '.')
            response.status_code = 400
            return response
        else:
            if info_trip.get('passenger_id') == client_id:
                #Veo si el viaje fue aceptado
                if info_trip.get('aceptoViaje'):
                    #Comienzo el viaje
                    response_mongo = MODEL_MANAGER.start_trip(trip_id)
                else:
                    response = jsonify(code=-5, message='El viaje ' + str(trip_id) +
                                       ' no fue aceptado por el chofer.')
                    response.status_code = 400
                    return response
            else:
                response = jsonify(code=-7, message='El viaje ' + str(trip_id) +
                                   ' no le pertenece al usuario ' + client_id + '.')
                response.status_code = 400
                return response
        if response_mongo:
            #Se pudo comenzar el viaje
            response = jsonify(code=0, message='El viaje ' + str(trip_id) +
                               ' ha comenzado.')
            response.status_code = 201
            return response
        else:
            response = jsonify(code=-1, message='El viaje ' + str(trip_id) +
                               ' no se pudo comenzar, vuelva a intentarlo mas tarde.')
            response.status_code = 400
            return response

    def finish_trip(self, client_id, trip_id):
        """ Este metodo indica que se comenzo un viaje
            @param client_id identificador del cliente
            @param trip_id identificador del viaje"""
        is_client = True
        info_user = MODEL_MANAGER.get_info_usuario(client_id)
        #Verificamos que el usuario sea un cliente
        if info_user == {}:
            response_shared_server = SHARED_SERVER.get_client(client_id)
            if response_shared_server.status_code != 200:
                #VER QUE OTROS ERRORES PUEDE DEVOLVER EL SHARED SERVER!!!
                #No existe el usuario
                response = jsonify(code=-5, message='El usuario ' + str(client_id) + ' no existe.')
                response.status_code = 404
                return response
            else:
                info_user = json.loads(response_shared_server.text).get('user')
                if info_user.get('type') != TIPO_CLIENTE:
                    is_client = False
                #Agrego la info a la base
                MODEL_MANAGER.add_usuario(client_id, info_user.get('type'),
                                          info_user.get('username'))
        else:
            if info_user.get('typeClient') != TIPO_CLIENTE:
                is_client = False
        if is_client is False:
            response = jsonify(code=-2, message='El usuario ' + str(client_id) +
                               ' no es un pasajero.')
            response.status_code = 400
            return response

        #Vamos a verificar que el viaje pertenezca al cliente
        response_mongo = False
        info_trip = MODEL_MANAGER.get_trip(trip_id)
        if info_trip is None:
            response = jsonify(code=-4, message='El viaje ' + str(trip_id) + ' no existe.')
            response.status_code = 404
            return response
        if info_trip.get('passenger_id') is None:
            response = jsonify(code=-7, message='El viaje ' + str(trip_id) +
                               ' no le pertenece al usuario ' + client_id + '.')
            response.status_code = 400
            return response
        else:
            if info_trip.get('passenger_id') == client_id:
                #Veo si el viaje fue comenzado
                if info_trip.get('startStamp') is None:
                    response = jsonify(code=-8, message='El viaje ' + str(trip_id) +
                                       ' no fue comenzado.')
                    response.status_code = 400
                    return response
                else:
                    #Termino el viaje
                    response_mongo = MODEL_MANAGER.end_trip(trip_id)
            else:
                response = jsonify(code=-7, message='El viaje ' + str(trip_id) +
                                   ' no le pertenece al usuario ' + client_id + '.')
                response.status_code = 400
                return response
        if response_mongo:
            #Se pudo finalizar el viaje asi que enviamos la informacion a SharedServer
            #VER SI HAY QUE MANDARLE MENOS INFORMACION!!!!!
            SHARED_SERVER.post_trip(info_trip)
            response = jsonify(code=0, message='El viaje ' + str(trip_id) +
                               ' ha finalizado.')
            response.status_code = 201
            return response
        else:
            response = jsonify(code=-1, message='El viaje ' + str(trip_id) +
                               ' no se pudo comenzar, vuelva a intentarlo mas tarde.')
            response.status_code = 400
            return response

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
        lat = data.get('lat')
        lon = data.get('long')
        accuracy = data.get('accuracy')
        operation_result = MODEL_MANAGER.add_last_known_position(user_id, lat, lon, accuracy)
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
        clients = MODEL_MANAGER.get_locations_by_type(type_client)
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
