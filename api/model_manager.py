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

    def add_last_known_position(self, user_id, user_type, lat, lon):
        """Este metodo graba en la base de datos 'UltimasPosiciones'
            la ultima posicion registrada del usuario.
            @param user_id el id del usuario
            @param user_type el tipo de usuario
            @param lat latitud en mapa
            @param lon longitud en mapa
        """
        #obtengo la tabla de ultimas posiciones
        ultimas_posiciones = self.db_manager.get_table('ultimasPosiciones')

        #busco si ya hay una posicion registrada para el usuario con esta id
        last_position = ultimas_posiciones.find_one({'idUsuario': user_id})

        if last_position.count() == 0:
            #no hay ultima posicion, entonces creo una nueva entrada
            nueva_posicion = {
                "idUsuario": user_id,
                "tipo_usuario": user_type,
                "lat": lat,
                "long": lon,
                "stamp": str(datetime.now())
            }

            #agrego la nueva posicion a la coleccion y devuelvo el resultado de la operacion
            return ultimas_posiciones.insert_one(nueva_posicion).acknowledged
        else:
            return ultimas_posiciones.update_one({
                '_id': str(last_position.get('_id'))
            }, {
                '$set': {
                    'lat': lat,
                    'long': lon
                }
            }, upsert=False).acknowledged

    def get_last_known_position(self, client_id):
        """Este metodo obtiene la ultima posicion conocida por
        el app server de un usuario"""

        #obtengo la coleccion
        ultimas_posiciones = self.db_manager.get_table('ultimasPosiciones')

        ultima_pos = ultimas_posiciones.find_one({'idUsuario': client_id})

        response = {
            "lat": str(ultima_pos.get('lat')),
            "long": str(ultima_pos.get('long')),
            "stamp": str(ultima_pos.get('stamp'))
        }

        return jsonify(response)