""" @package test.mongo_model_test
"""
import unittest
import json
import main_app
from flask import jsonify
from api.model_manager import ModelManager

class TestMongoMOdel(unittest.TestCase):
    """ Esta clase tiene los test de los metodos de manipulacion del modelo en MongoDB
    """

    def setUp(self):
        self.app = main_app.application.test_client()
        self.app.testing = True
        self.model_manager = ModelManager()

    def test_add_get_usuario(self):
        """Se prueban las operaciones de Alta, Baja, y Modificacion de Usuario"""
        user_id = 28
        user_type = "driver"
        username = "Nico"
        self.assertTrue(self.model_manager.add_usuario(user_id, user_type, username))
        #Testeo que se haya guardado bien obteniendo devuelta al usuario
        recovered_user = self.model_manager.get_info_usuario(user_id)
        self.assertEqual(recovered_user.get('username'), username)
        self.assertEqual(recovered_user.get('typeClient'), user_type)
        #Borro el usuario creado
        self.assertTrue(self.model_manager.delete_usuario(user_id))
