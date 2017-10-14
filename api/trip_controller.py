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
        #Hay que filtrar los usuarios por tipos
        json_data = json.loads(response_shared_server.text)
        json_response = json_data['paymethods']
        response = jsonify(json_response)
        response.status_code = response_shared_server.status_code
        return response
