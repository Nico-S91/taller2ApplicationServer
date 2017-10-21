""" @package api.transaction_controller
"""
import json
from flask import jsonify
from service.shared_server import SharedServer
from service.shared_server import TIPO_CLIENTE
from service.shared_server import TIPO_CHOFER

SHARED_SERVER = SharedServer()

class TransactionController:
    """Esta clase se va a encargar de manejar las transacciones de los clientes"""

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

    def get_transactions(self, id_user):
        """Este metodo devuelve la informacion de todas las transacciones de un usuario"""
        response_shared_server = SHARED_SERVER.get_transactions(id_user)
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 200:
            json_response = json_data['transactions']
        else:
            json_response = json_data
        response = jsonify(json_response)
        response.status_code = response_shared_server.status_code
        return response

    def post_transactions(self, transaction, id_user):
        """ Este metodo permite guardar la informacion de una transaccion de un usuario
            @param transaction informacion de la transaccion
            @param id_user identificador del usuario"""
        response_shared_server = SHARED_SERVER.post_transactions(transaction, id_user)
        json_data = json.loads(response_shared_server.text)
        if response_shared_server.status_code == 200:
            json_response = json_data['transaction']
        else:
            json_response = json_data
        response = jsonify(json_response)
        response.status_code = response_shared_server.status_code
        return response
