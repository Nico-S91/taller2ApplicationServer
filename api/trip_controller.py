""" @package api.trip_controller
"""
import json
from flask import jsonify
from service.shared_server import SharedServer

SHARED_SERVER = SharedServer()

class TripController:
    """Esta clase tiene los metodos para manajar la informacion de los viajes"""

    def __init__(self):
        """The constructor."""
        self.refs = {}

    def get_payment_methods(self):
        """Este metodo devuelve la informacion de todos los medios de pago"""
        response_shared_server = SHARED_SERVER.get_payment_methods()
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 200:
            json_response = json_data['paymethods']
        else:
            json_response = json_data
        response = jsonify(json_response)
        response.status_code = response_shared_server.status_code
        return response
