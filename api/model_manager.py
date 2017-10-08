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
            @param user_id identificador de usuario"""
        
        #obtengo la tabla usuarios
        usuarios = self.db_manager.get_table('usuarios')
        nuevo_usuario = {
            "username": username,
            "idUsuario": user_id
        }

        #obtengo el id del usuario creado
        id_nuevo_usuario = usuarios.insert_one(nuevo_usuario).inserted_id

        return id_nuevo_usuario

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
