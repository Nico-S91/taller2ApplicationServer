""" @package model_manager
"""
from datetime import datetime
from flask import jsonify
import model.db_manager

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
        user_info = usuarios.find_one({'idUsuario': user_id})

        if user_info is None:
            return {}
        else:
            response = {
                'username': str(user_info.get('username')),
                'typeClient': str(user_info.get('typeClient'))
            }
            return response

    def add_usuario(self, user_id, user_type, username):
        """Este metodo agrega un usuario a la coleccion de usuarios en Mongo
            @param user_id el id del nuevo usuario
            @param user_type el tipo de usuario (chofer o pasajero)
            @param username su nickname
        """

        #creo el nuevo user
        new_user = {
            "username": username,
            "idUsuario": user_id,
            "typeClient": user_type
        }

        usuarios = self.db_manager.get_table('usuarios')
        return usuarios.insert_one(new_user).acknowledged

    def delete_usuario(self, user_id):
        """ Este metodo elimina un usuario de la coleccion de usuarios en Mongo
            @param user_id un id de usuario
        """

        usuarios = self.db_manager.get_table('usuarios')
        return usuarios.delete_one({'idUsuario': user_id}).acknowledged

    def add_trip(self, info_viaje):
        """Este metodo guarda la informacion de un nuevo viaje publicado
            @param info_viaje un dictionary con la info del viaje
        """

        viajes = self.db_manager.get_table('viajes')

        new_viaje = {
            "idViaje": info_viaje.get("trip_id"),
            "idDriver": info_viaje.get("driver"),
            "idPassenger": info_viaje.get("passenger"),
            "trip": info_viaje.get("trip"),
            "paymethod": info_viaje.get("paymethod"),
            "route": [],
            "aceptoViaje": info_viaje.get("accepted")
        }

        return viajes.insert_one(new_viaje).acknowledged

    def get_locations_by_type(self, client_type):
        """ Este metodo devuelve un array de ubicaciones de todos los clientes
            con el tipo dado con su id y el par <latitud, longitud>
            @param client_type el tipo de cliente
        """
        result = []

        #Obtengo todos los usuarios del tipo client_type
        usuarios = self.db_manager.get_table('usuarios')
        usuarios_by_tipo = usuarios.find({'typeClient': client_type}, {"_id": 0, "idUsuario": 1})

        ubicaciones = self.db_manager.get_table('ubicaciones')

        for user_id in usuarios_by_tipo:
            last_location = ubicaciones.find_one({'idUsuario': user_id})
            if last_location is not None:
                new_last_location = {
                    "client_id": user_id,
                    "lat": last_location.get('lat'),
                    "long": last_location.get('long')
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
        viaje = viajes.find_one({'idViaje': trip_id})

        if viaje is not None:
            locations = viaje.get('route')
            new_location = {
                "location": {
                    "lat": location.get('lat'),
                    "long": location.get('long')
                },
                "timestamp": datetime.datetime.now().date()
            }
            locations.append(new_location)
            result = viajes.update_one({'_id': viaje.get('_id')}, {'$set': {'route': locations}}, upsert=False).acknowledged
        
        return result

    def get_trip(self, trip_id):
        """ Este metodo obtiene el viaje dado su id
            @param trip_id el id del viaje
        """

        viajes = self.db_manager.get_table('viajes')
        viaje = viajes.find_one({'idViaje': trip_id})

        if viaje is not None:
            response = {
                "trip_id": viaje.get('idViaje'),
                "driver_id": viaje.get('idDriver'),
                "passenger_id": viaje.get('idPassenger'),
                "trip": viaje.get('trip'),
                "paymethod": viaje.get('paymethod'),
                "route": viaje.get('route'),
                "aceptoViaje": viaje.get('aceptoViaje')
            }
            return response

        return None

    def delete_trip(self, trip_id):
        """ Este metodo elimina un viaje
            @param trip_id el id del viaje
        """

        viajes = self.db_manager.get_table('viajes')
        return viajes.delete_one({'idViaje': trip_id}).acknowledged

    def start_trip(self, trip_id):
        """ Este metodo inicia el timestamp del atributo start de un viaje
            @param trip_id el id del viaje
        """

        viajes = self.db_manager.get_table('viajes')
        viaje = viajes.find_one({'idViaje': trip_id})

        if viaje is not None:
            return viajes.update_one({'_id': viaje.get('_id')}, {'$set': {'startStamp': datetime.datetime.now()}}, upsert=False).acknowledged

        return False

    def end_trip(self, trip_id):
        """ Este metodo termina, y marca con un timestamp del atributo end de un viaje
            @param trip_id el id del viaje
        """

        viajes = self.db_manager.get_table('viajes')
        viaje = viajes.find_one({'idViaje': trip_id})

        if viaje is not None:
            return viajes.update_one({'_id': viaje.get('_id')}, {'$set': {'endStamp': datetime.datetime.now()}}, upsert=False).acknowledged

        return False

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

        #busco si ya hay una posicion registrada para el usuario con esta id
        ultima_ubicacion = ubicaciones.find_one({'idUsuario': user_id})

        if ultima_ubicacion is None:
            #no hay ultima posicion, entonces creo una nueva entrada
            nueva_posicion = {
                "idUsuario": user_id,
                "timestamp": str(datetime.now()),
                "lat": latitud,
                "long": longitud,
                "accuracy": accuracy
            }

            #agrego la nueva posicion a la coleccion y devuelvo el resultado de la operacion
            return ubicaciones.insert_one(nueva_posicion).acknowledged
        else:
            return ubicaciones.update_one({
                '_id': str(ultima_ubicacion.get('_id'))
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

        ultima_ubicacion = ubicaciones.find_one({'idUsuario': client_id})

        response = {
            "lat": str(ultima_ubicacion.get('lat')),
            "long": str(ultima_ubicacion.get('long')),
            "accuracy": str(ultima_ubicacion.get('accuracy')),
            "stamp": str(ultima_ubicacion.get('stamp'))
        }

        return jsonify(response)

    def add_driver_to_trip(self, trip_id,  driver_id):
        """ Este metodo agrega el chofer asignado a un viaje.
            @param trip_id el id del viaje
            @param driver_id el id del chofer asignado
        """

        viajes = self.db_manager.get_table('viajes')
        viaje = viajes.find_one({'idViaje': trip_id})

        if viaje is not None:
            return viajes.update_one({'_id': viaje.get('_id')}, {'$set': {'idDriver': driver_id}}, upsert=False).acknowledged
        else:
            return False
    
    def accept_trip(self, trip_id):
        """ Este metodo tilda al viaje como aceptado
            @param trip_id el id del viaje
        """

        viajes = self.db_manager.get_table('viajes')
        viaje = viajes.find_one({'idViaje': trip_id})

        if viaje is not None:
            return viajes.update_one({'_id': viaje.get('_id')}, {'$set': {'aceptoViaje': True}}, upsert=False).acknowledged
        else:
            return False
