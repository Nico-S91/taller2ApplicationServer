""" @package model_manager
"""
from datetime import datetime
from flask import jsonify
import model.db_manager
from bson.objectid import ObjectId
import json
import bson

class ModelManager:
    """Esta clase contiene los metodos para operar con las tablas
    del modelo del application server"""

    def __init__(self):
        """constructor"""
        self.db_manager = model.db_manager

    def get_info_usuario(self, user_id):
        """Este metodo obtiene la informacion de un usuario en base de datos de Mongo
            @param user_id id del usuario
        """
        usuarios = self.db_manager.get_table('usuarios')
        if usuarios is None:
            return None

        user_info = usuarios.find_one({'user_id': user_id})

        if user_info is None:
            return None
        else:
            response = {
                'username': str(user_info['username']),
                'client_type': str(user_info['client_type'])
            }
            return response

    def add_usuario(self, user_id, user_type, username, available):
        """Este metodo agrega un usuario a la coleccion de usuarios en Mongo
            @param user_id el id del nuevo usuario
            @param user_type el tipo de usuario (chofer o pasajero)
            @param username su nickname
            @param available si el usuario esta disponible
        """
        if available is None:
            available = True

        #creo el nuevo user
        new_user = {
            "username": username,
            "user_id": user_id,
            "client_type": user_type,
            "available": available
        }

        usuarios = self.db_manager.get_table('usuarios')
        if usuarios is None:
            return False

        return usuarios.insert_one(new_user).acknowledged

    def update_usuario(self, user_id, user_type, username, available):
        """ Este metodo actualiza a un usuario con la informacion ingresada
            @param user_id el id del usuario
            @param user_type el tipo de usuario
            @param username nombre de usuario
            @param available si el usuario esta disponible
        """
        usuarios = self.db_manager.get_table('usuarios')
        if usuarios is None:
            return False

        user_to_update = usuarios.find_one({'user_id': user_id})

        return usuarios.update_one({'_id': user_to_update.get('_id')},
                                   {'$set': {'user_type': user_type,
                                             'username': username, 'available': available}},
                                   upsert=False).acknowledged

    def delete_usuario(self, user_id):
        """ Este metodo elimina un usuario de la coleccion de usuarios en Mongo
            @param user_id un id de usuario
        """
        usuarios = self.db_manager.get_table('usuarios')
        if usuarios is None:
            return True

        return usuarios.delete_one({'user_id': user_id}).acknowledged

    def get_usuarios(self):
        """ Este metodo obtiene todos los usuarios de mongo"""
        usuarios = self.db_manager.get_table('usuarios')
        if usuarios is None:
            return []

        lista_usuarios = usuarios.find({}, {"_id": 0})

        if lista_usuarios is None:
            return []
        else:
            result = []
            for usuario in lista_usuarios:
                result.append(usuario)
            return result

    def change_available_driver(self, user_id, available):
        """ Este metodo modifica la disponibilidad del usuario
            @param user_id id del usuario
            @param available es un boolean que indica si esta o no disponible
        """
        usuarios = self.db_manager.get_table('usuarios')
        if usuarios is None:
            return None

        user_data = usuarios.find_one({'user_id': user_id})

        return usuarios.update_one({'_id': user_data.get('_id')},
                                   {'$set': {'available': available}},
                                   upsert=False).acknowledged


    def user_is_available(self, user_id):
        """ Este metodo devuelve verdadero si el usuario esta disponible o falso sino
            @param user_id id del usuario
        """
        usuarios = self.db_manager.get_table('usuarios')
        if usuarios is None:
            return None

        user_data = usuarios.find_one({'user_id': user_id})

        return user_data.get('available')

    def add_trip(self, info_viaje):
        """Este metodo guarda la informacion de un nuevo viaje publicado
            @param info_viaje un dictionary con la info del viaje
        """

        viajes = self.db_manager.get_table('viajes')
        if viajes is None:
            return None

        trip_info = info_viaje["trip"]
        driver_id = trip_info["driver"]
        passenger_id = trip_info["passenger"]

        new_viaje = {
            "driver_id": driver_id,
            "passenger_id": passenger_id,
            "trip": info_viaje["trip"],
            "paymethod": info_viaje["paymethod"],
            "accepted_route": info_viaje["accepted_route"],
            "route": [],
            "is_accepted": False
        }

        result = viajes.insert_one(new_viaje).acknowledged
        if not result:
            return None
        print('Se creo el viaje...')
        trip_data = viajes.find_one(new_viaje)
        if trip_data is None:
            return None
        print('Obtuve el viaje y ahora pido el id!!!')
        return trip_data.get('_id')

    def get_locations_by_type(self, client_type):
        """ Este metodo devuelve un array de ubicaciones de todos los clientes
            con el tipo dado con su id y el par <latitud, longitud>
            @param client_type el tipo de cliente
        """
        result = []

        #Obtengo todos los usuarios del tipo client_type
        usuarios = self.db_manager.get_table('usuarios')
        if usuarios is None:
            return result

        usuarios_by_tipo = usuarios.find({'client_type': client_type}, {"_id": 0, "user_id": 1})

        ubicaciones = self.db_manager.get_table('ubicaciones')
        if ubicaciones is None:
            return result

        for user in usuarios_by_tipo:
            user_id = user.get('user_id')
            last_location = ubicaciones.find_one({'user_id': user_id})
            if last_location is not None:
                new_last_location = {
                    "user_id": user_id,
                    "lat": last_location.get('lat'),
                    "long": last_location.get('long'),
                    "accuracy": last_location.get('accuracy')
                }
                result.append(new_last_location)
        return result

    def add_location_to_trip(self, location, trip_id):
        """ Este metodo agrega una ubicacion a un viaje
            @param location una ubicacion
            @param trip_id el id del viaje
        """
        result = False
        viajes = self.db_manager.get_table('viajes')
        if viajes is None:
            return result

        viaje = viajes.find_one({'_id': ObjectId(trip_id)})
        lat = location.get('lat')
        lon = location.get('long')

        if lat is None or lon is None:
            return result

        if viaje is not None:
            locations = viaje.get('route')
            new_location = {
                "location": {
                    "lat": lat,
                    "long": lon
                },
                "timestamp": datetime.now().date()
            }
            locations.append(new_location)
            result = viajes.update_one({'_id': viaje.get('_id')},
                                       {'$set': {'route': locations}}, upsert=False).acknowledged

        return result

    def get_trip(self, trip_id):
        """ Este metodo obtiene el viaje dado su id
            @param trip_id el id del viaje
        """
        if not bson.objectid.ObjectId.is_valid(trip_id):
            return None
        viajes = self.db_manager.get_table('viajes')
        if viajes is None:
            return None

        viaje = viajes.find_one({'_id': ObjectId(trip_id)})

        if viaje is not None:
            response = {
                "trip_id": str(viaje.get('_id')),
                "driver_id": viaje.get('driver_id'),
                "passenger_id": viaje.get('passenger_id'),
                "trip": viaje.get('trip'),
                "paymethod": viaje.get('paymethod'),
                "route": viaje.get('route'),
                "is_accepted": viaje.get('is_accepted'),
                "is_refused": viaje.get('is_refused'),
                "start_stamp": str(viaje.get('start_stamp')),
                "end_stamp": str(viaje.get('end_stamp'))
            }
            return response
        return None

    def delete_trip(self, trip_id):
        """ Este metodo elimina un viaje
            @param trip_id el id del viaje
        """

        viajes = self.db_manager.get_table('viajes')
        if viajes is None:
            return True

        return viajes.delete_one({'_id': trip_id}).acknowledged

    def start_trip(self, trip_id):
        """ Este metodo inicia el timestamp del atributo start de un viaje
            @param trip_id el id del viaje
        """

        viajes = self.db_manager.get_table('viajes')
        if viajes is None:
            return False

        viaje = viajes.find_one({'_id': ObjectId(trip_id)})

        if viaje is not None:
            return viajes.update_one({'_id': viaje.get('_id')}, {'$set': {'start_stamp': datetime.now()}}, upsert=False).acknowledged

        return False
    
    def end_trip(self, trip_id):
        """ Este metodo termina, y marca con un timestamp del atributo end de un viaje
            @param trip_id el id del viaje
        """
        viajes = self.db_manager.get_table('viajes')
        if viajes is None:
            return False

        viaje = viajes.find_one({'_id': ObjectId(trip_id)})

        if viaje is not None:
            return viajes.update_one({'_id': viaje.get('_id')}, {'$set': {'end_stamp': datetime.now()}}, upsert=False).acknowledged

        return False

    # def put_trip_new_driver(self, trip_id, driver_id):
    #     """ Este metodo modifica el chofer de un viaje
    #         @param trip_id es el identificador del viaje
    #         @param driver_id es el identificador del chofer
    #     """
    #     viajes = self.db_manager.get_table('viajes')
    #     if viajes is None:
    #         return False

    #     viaje = viajes.find_one({'_id': ObjectId(trip_id)})

    #     if viaje is not None:
    #         trip = viaje.get('trip')
    #         trip.driver_id = driver_id
    #         return viajes.update_one({'_id': viaje.get('_id')}, {'$set': {'driver_id':driver_id, 'trip':trip}}, upsert=False).acknowledged

    #     return False

    def add_last_known_position(self, user_id, latitud, longitud, accuracy):
        """ Este metodo graba en la base de datos 'UltimasPosiciones'
            la ultima posicion registrada del usuario.
            @param user_id el id del usuario
            @param latitud latitud en mapa
            @param longitud longitud en mapa
            @param accuracy el radio de precision
        """
        #obtengo la tabla de ultimas posiciones
        ubicaciones = self.db_manager.get_table('ubicaciones')
        if ubicaciones is None:
            return False

        #busco si ya hay una posicion registrada para el usuario con esta id
        ultima_ubicacion = ubicaciones.find_one({'user_id': user_id})

        if ultima_ubicacion is None:
            #no hay ultima posicion, entonces creo una nueva entrada
            nueva_posicion = {
                "user_id": user_id,
                "timestamp": str(datetime.now()),
                "lat": latitud,
                "long": longitud,
                "accuracy": accuracy
            }

            #agrego la nueva posicion a la coleccion y devuelvo el resultado de la operacion
            return ubicaciones.insert_one(nueva_posicion).acknowledged
        else:
            return ubicaciones.update_one({
                '_id': ultima_ubicacion.get('_id')
            }, {
                '$set': {
                    'lat': latitud,
                    'long': longitud,
                    'accuracy': accuracy
                }
            }, upsert=False).acknowledged

    def get_last_known_position(self, client_id):
        """Este metodo obtiene la ultima posicion conocida por
            el app server de un usuario
            @param client_id el id del cliente
        """

        #obtengo la coleccion
        ubicaciones = self.db_manager.get_table('ubicaciones')
        if ubicaciones is None:
            return None

        ultima_ubicacion = ubicaciones.find_one({'user_id': client_id})

        if ultima_ubicacion is None:
            return None

        response = {
            "lat": str(ultima_ubicacion.get('lat')),
            "long": str(ultima_ubicacion.get('long')),
            "accuracy": str(ultima_ubicacion.get('accuracy')),
            "timestamp": str(ultima_ubicacion.get('timestamp'))
        }

        return response

    def add_driver_to_trip(self, trip_id,  driver_id):
        """ Este metodo agrega el chofer asignado a un viaje.
            @param trip_id el id del viaje
            @param driver_id el id del chofer asignado
        """

        viajes = self.db_manager.get_table('viajes')
        if viajes is None:
            return False

        viaje = viajes.find_one({'_id': ObjectId(trip_id)})

        if viaje is not None:
            trip = viaje.get('trip')
            trip.driver_id = driver_id
            return viajes.update_one({'_id': viaje.get('_id')}, {'$set': {'driver_id':driver_id, 'trip':trip}}, upsert=False).acknowledged
        else:
            return False
    
    def accept_trip(self, trip_id):
        """ Este metodo tilda al viaje como aceptado
            @param trip_id el id del viaje
        """

        viajes = self.db_manager.get_table('viajes')
        if viajes is None:
            return False

        viaje = viajes.find_one({'_id': ObjectId(trip_id)})

        if viaje is not None:
            return viajes.update_one({'_id': viaje.get('_id')}, {'$set': {'is_accepted': True}}, upsert=False).acknowledged
        else:
            return False

    def refuse_trip(self, trip_id):
        """ Este metodo tilda al viaje como rechazado
            @param trip_id el id del viaje
        """
        viajes = self.db_manager.get_table('viajes')
        if viajes is None:
            return False

        viaje = viajes.find_one({'_id': ObjectId(trip_id)})

        if viaje is not None:
            trip = viaje.get('trip')
            trip.driver_id = None
            return viajes.update_one({'_id': viaje.get('_id')}, {'$set': {'driver':None ,'is_refused': True, 'trip':trip}}, upsert=False).acknowledged
        else:
            return False

    def get_trip_without_drivers(self):
        """Este metodo devuelve los viajes que no tienen idDriver asignado"""

        viajes = self.db_manager.get_table('viajes')
        if viajes is None:
            return []

        viajes_sin_driver = viajes.find({'driver_id': None}, {"_id": 0})

        if viajes_sin_driver is None:
            return []
        else:
            result = []
            for trip in viajes_sin_driver:
                result.append(trip)
            return result

    def get_trips_with_driver_id(self, driver_id):
        """ Este metodo devuelve todos los viajes con el id del driver pedido
            @param driver_id el id de driver
        """

        viajes = self.db_manager.get_table('viajes')
        if viajes is None:
            return []

        viajes_con_id_driver = viajes.find({'driver_id': driver_id}, {"_id": 0})

        if viajes_con_id_driver is None:
            return []
        else:
            result = []
            for trip in viajes_con_id_driver:
                result.append(trip)
            return result

    def get_started_and_unfinished_trips_with_driver_id(self, driver_id):
        """ Este metodo devuelve todos los viajes con el id del driver pedido 
            que comenzaron pero aun no finalizaron
            @param driver_id el id de driver
        """

        viajes = self.db_manager.get_table('viajes')
        if viajes is None:
            return []

        viajes_sin_terminar = viajes.find({'driver_id':{"$exists": True},
                                           'end_stamp': None}, {"_id": 0})

        if viajes_sin_terminar is None:
            return []
        else:
            result = []
            for trip in viajes_sin_terminar:
                if trip.get('start_stamp') is not None:
                    result.append(trip)
            return result

    def get_unfinished_trips(self):
        """ Este metodo devuelve los viajes en mongo sin stamp de end"""

        viajes = self.db_manager.get_table('viajes')
        if viajes is None:
            return []

        viajes_sin_terminar = viajes.find({'driver_id':{"$exists": True}, 'start_stamp': None}, {"_id": 0})

        if viajes_sin_terminar is None:
            return []
        else:
            result = []
            for trip in viajes_sin_terminar:
                result.append(trip)
            return result

    def trips_by_client(self, client_id):
        """ Este metodo devuelve los viajes asociados con el id de un cliente
            @param client_id el id del cliente
        """

        viajes = self.db_manager.get_table('viajes')
        if viajes is None:
            return []

        viajes_con_id_client = viajes.find({'passenger_id': client_id}, {"_id": 0})

        if viajes_con_id_client is None:
            return []
        else:
            result = []
            for trip in viajes_con_id_client:
                result.append(trip)
            return result
