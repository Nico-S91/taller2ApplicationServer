""" @package model_manager
"""
from flask import jsonify
import model.db_manager

class ModelManager:
    """Esta clase tiene los metodos para operar con las tablas del modelo del application server"""

    def __init__(self):
        """Constructor"""
        self.db_manager = model.db_manager
 
    def add_user(self, username, user_id):
        """Este metodo graba en la base de datos USUARIOS un nuevo usuario.
            @param username nombre de usuario
            @param user_id identificador de usuario
        """
        #obtengo la tabla usuarios
        usuarios = self.db_manager.get_table('usuarios')
        nuevo_usuario = {
            "username": username,
            "idUsuario": user_id
        }

        #obtengo el id del usuario creado
        id_nuevo_usuario = usuarios.insert_one(nuevo_usuario).inserted_id

        return id_nuevo_usuario

    def get_user(self, user_id):
        """ Este metodo obtiene a un usuario de la coleccion Usuarios
            @param user_id el id de usuario a buscar
        """
        usuarios = self.db_manager.get_table('usuarios')

        user = usuarios.find_one({'idUsuario': user_id})

        response = {
            "_id": str(user.get('_id')),
            "idUsuario": user.get('idUsuario'),
            "username": user.get('username')
        }

        return jsonify(response)

    def remove_user(self, user_id):
        """ Este metodo elimina a un usuario de la coleccion USUARIOS.
            @param user_id id del usuario a eliminar
        """
        usuarios = self.db_manager.get_table('usuarios')

        delete_info = usuarios.delete_one({'idUsuario': user_id})
        response = {
            "operation_result": delete_info.acknowledged,
            "delete_count": delete_info.deleted_count
        }

        return jsonify(response)

    def add_auth_token(self, user_id, token, expiration):
        """ Este metodo graba en la base de datos OauthToken un nuevo token de autorizacion.
            @param user_id identificador de usuario
            @param token un token de autorizacion
            @param expiration fecha de expiracion del token
        """
        auth_tokens = self.db_manager.get_table('OauthToken')

        nuevo_token = {
            "idusuario": user_id,
            "token": token,
            "expiration": expiration
        }

        id_nuevo_token = auth_tokens.insert_one(nuevo_token).inserted_id

        return id_nuevo_token

    def get_auth_token(self, token):
        """ Este metodo obtiene a un token de la coleccion OauthToken
            @param token el nombre del token
        """
        auth_tokens = self.db_manager.get_table('OauthToken')

        token = auth_tokens.find_one({'token': token})

        response = {
            "_id": str(token.get('_id')),
            "idusuario": token.get('idusuario'),
            "token": token.get('token'),
            "expiration": token.get('expiration'),
        }

        return jsonify(response)

    def delete_token(self, token):
        """ Este metodo elimina un token, al proveer el nombre del mismo
            @param token nombre del token a eliminar
        """
        auth_tokens = self.db_manager.get_table('OauthToken')

        delete_info = auth_tokens.delete_one({'token': token})
        response = {
            "operation_result": delete_info.acknowledged,
            "delete_count": delete_info.deleted_count
        }

        return jsonify(response)

    def add_credenciales_ubicacion(self, user_id, key_geolocation):
        """Este metodo graba en la base de datos de credenciales de ubicacion una nueva key.
            @param user_id identificador de usuario
            @param key_geolocation la llave asociada
        """
        credenciales = self.db_manager.get_table('CredencialesUbicacion')

        nueva_credencial = {
            "idusuario": user_id,
            "keyGeolocation": key_geolocation
        }

        id_nueva_credencial = credenciales.insert_one(nueva_credencial).inserted_id

        return id_nueva_credencial

    def get_credenciales_ubicacion(self, user_id):
        """ Este metodo obtiene TODAS las credenciales de ubicacion dado un user_id
            @param user_id un id de usuario
        """
        credenciales = self.db_manager.get_table('CredencialesUbicacion')

        cred_asociadas = credenciales.find({'idusuario': user_id})

        response = []
        for credencial in cred_asociadas:
            newobj = {
                "key": credencial.get('keyGeolocation')
            }
            response.append(newobj)

        return jsonify(response)
    