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
        """Se prueban las operaciones de Alta, Baja y Modificacion de Usuario"""
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

    def test_add_get_viaje(self):
        """Se prueban las operaciones de Alta, Baja y Modificacion de Viaje"""
        trip_info = '{\r\n  \"trip\": {\r\n    \"driver\": \"string\",\r\n    \"passenger\": \"string\",\r\n    \"start\": {\r\n      \"address\": {\r\n        \"street\": \"string\",\r\n        \"location\": {\r\n          \"lat\": 0,\r\n          \"lon\": 0\r\n        }\r\n      }\r\n    },\r\n    \"end\": {\r\n      \"address\": {\r\n        \"street\": \"string\",\r\n        \"location\": {\r\n          \"lat\": 0,\r\n          \"lon\": 0\r\n        }\r\n      }\r\n    },\r\n    \"distance\": 0\r\n  }\r\n}'
        pay_method = '{\r\n    \"paymethod\": \"string\",\r\n    \"parameters\": {}\r\n  }'
        viaje = {
            "trip_id": 1,
            "driver": 28,
            "passenger": 10,
            "trip": trip_info,
            "paymethod": pay_method,
            "accepted": False
        }

        self.assertTrue(self.model_manager.add_trip(viaje))
        recovered_trip = self.model_manager.get_trip(1)

        # print(str(recovered_trip.get("trip_id")))
        # print(str(recovered_trip.get("driver_id")))
        # print(str(recovered_trip.get("passenger_id")))
        # print(str(recovered_trip.get("trip")))
        # print(str(recovered_trip.get("paymethod")))
        # print(str(recovered_trip.get("route")))
        # print(str(recovered_trip.get("aceptoViaje")))
        self.assertEqual(recovered_trip.get('trip_id'), 1)
        self.assertEqual(recovered_trip.get('driver_id'), 28)
        self.assertEqual(recovered_trip.get('passenger_id'), 10)
        self.assertEqual(recovered_trip.get('trip'), trip_info)
        self.assertEqual(recovered_trip.get('paymethod'), pay_method)
        self.assertEqual(recovered_trip.get('route'), [])
        self.assertEqual(recovered_trip.get('aceptoViaje'), False)
        self.assertTrue(self.model_manager.delete_trip(viaje))
