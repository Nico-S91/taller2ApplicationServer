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
                                          info_user.get('username'), True)
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
                                          info_user.get('username'), True)
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
                                          info_user.get('username'), True)
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

    def get_available_trips(self, user_id):
        """ Este metodo valida el id del usuario, y si es un driver valido, devuelve los 
            viajes disponibles al driver, junto con los ya aceptados por este
        """
        check_valid_driver = self._validate_user_with_type(user_id, "driver")

        if not check_valid_driver:
            json_response = json.loads("""{
                    "mensaje": "Driver no existente"
                }""")
            response = jsonify(json_response)
            response.status_code = 400
            return response
        else:
            #el driver existe, devuelvo los trips SIN idDriver y los que tienen el mismo idDriver
            trips_sin_driver = MODEL_MANAGER.get_trip_without_drivers()
            trips_con_este_driver = MODEL_MANAGER.get_trips_with_driver_id(user_id)
            trips_merge = trips_sin_driver + trips_con_este_driver
            response = {
                "trips": trips_merge
            }
            
            return jsonify(response)

    def post_new_trip(self, data):
        """ Este metodo crea un nuevo viaje y lo almacena en la base de datos de MongoDB"""
        json_data = data

        check_driver = self._validate_user_with_type(json_data['idDriver'], "driver")
        check_passenger = self._validate_user_with_type(json_data['idPassenger'], "passenger")
        check_valid_trip = self._validate_trip_data(json_data['trip'])
        check_valid_accepted_route = self._validate_accepted_route(json_data['acceptedroute'])

        if not check_driver or not check_passenger or not check_valid_trip or not check_valid_accepted_route:
            json_data = json.loads("""{
                    "mensaje": "Invalid request"
                }""")
            response = jsonify(json_data)
            response.status_code = 400
            return response

        operation_result = MODEL_MANAGER.add_trip(json_data)
        if operation_result:
            json_data = json.loads("""{
                    "mensaje": "Se creo el viaje Correctamente"
                }""")
            response = jsonify(json_data)
            response.status_code = 201
            return response
        else:
            json_data = json.loads("""{
                    "mensaje": "Error de carga de viaje"
                }""")
            response = jsonify(json_data)
            response.status_code = 500
            return response

    def get_last_location(self, user_id):
        """ Devuelve response de ultima ubicacion
            @param user_id un id de usuario
        """
        response = MODEL_MANAGER.get_last_known_position(user_id)
        response.status_code = 200
        return response

    def get_mongo_users(self):
        """ Devuelve los usuarios de mongo"""
        response = jsonify(MODEL_MANAGER.get_usuarios())
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

    def post_new_app_user(self, data):
        """ Guarda en mongo los datos de un nuevo usuario
            @param data el json de request para dar de alta el usuario
        """
        user_id = data.get('user_id')
        username = data.get('username')
        user_type = data.get('user_type')

        operation_result = MODEL_MANAGER.add_usuario(user_id, user_type, username, True)
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

    def get_trips_by_client(self, client_id):
        """ Este metodo devuelve los viajes asociados con un cliente
            @param client_id el id del pasajero
        """
        trips = MODEL_MANAGER.trips_by_client(client_id)
        response = {
            "trips": trips
        }

        return jsonify(response)

    def get_trips_by_driver(self, driver_id):
        """ Este metodo devuelve los viajes asociados con un driver
            @param driver_id el id del chofer
        """
        trips = MODEL_MANAGER.get_trips_with_driver_id(driver_id)
        response = {
            "trips": trips
        }

        return jsonify(response)

    def get_ongoing_trips(self):
        """ Este metodo devuelve los viajes que aun no han finalizado"""
        trips = MODEL_MANAGER.get_unfinished_trips()
        response = {
            "trips": trips
        }

        return jsonify(response)

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

    def _validate_user_with_type(self, user_id, user_type):
        """ Valida la existencia de un usuario del tipo pedido, primero con Mongo,
            si no lo encuentra, en el shared, si esta lo crea en mongo, y si no existe
            devuelve invalido
            @param user_type
        """
        #Primero verifico si el usuario existe en Mongo y tiene el tipo correcto
        model_manager_response = MODEL_MANAGER.get_info_usuario(user_id)

        if model_manager_response is not None:
            if model_manager_response['typeClient'] == user_type:
                #Existe y tiene tipo valido
                return True
            else:
                #El cliente existe, pero no tiene el tipo correcto
                return False
        else:
            #si no esta en mongo, hay que buscar en la base de martin
            response_shared_server = SHARED_SERVER.get_client(user_id)
            json_data = json.loads(response_shared_server.text)
            if response_shared_server.status_code == 200:
                user_data = json_data['user']
                client_type = user_data['type']
                username = user_data['username']
                if client_type == user_type:
                    #Creo el usuario en mongo para tenerlo
                    MODEL_MANAGER.add_usuario(user_id, user_type, username, True)
                    return True
                else:
                    return False
            else:
                return False
                

    def _validate_trip_data(self, trip_info):
        """ Este metodo valida que los contenidos dentro de trip, en particular el
            start y end no esten vacios
            @param trip_info el diccionario de trip
        """
        flag_start = False
        flag_end = False

        if trip_info['start'] != None:
            flag_start = True

        if trip_info['end'] != None:
            flag_end = True

        return (flag_start and flag_end)

    def _validate_accepted_route(self, route):
        """ Este metodo valida la ruta acordada con el conductor
            @param route una ruta de google directions api
        """

        return route != None
