""" @package client_controller
"""
from resource.shared_server import SharedServer
from model.client_shared import ClientShared
from flask import jsonify

SHARED_SERVER = SharedServer()

class ClientController:
    """Esta clase tiene los metodos para manajar la informacion de los clientes"""

    def __init__(self):
        """The constructor."""
        self.ref = ""

    def get_info_new_client(self):
        """ Este metodo solo sirve para las pruebas"""
        client = ClientShared.new_client(1, "cliente", "Khaleesi", "Dragones3", "fb_user_id",
                                         "fb_auth_token", "Daenerys", "Targaryen", "Valyria",
                                         "madre_dragones@got.com", "01/01/1990")
        return client.get_json_new_client()

    def get_client(self, client_id):
        """ Este metodo devuelve la informacion del cliente buscado
            @param client_id es el id del cliente que se esta buscando la informacion"""
        informacion = SHARED_SERVER.get_client(client_id)
        return jsonify(
            client_id=informacion.client_id,
            type_client=informacion.type_client,
            username=informacion.username,
            fb_user_id=informacion.fb_user_id,
            fb_auth_token=informacion.fb_auth_token,
            first_name=informacion.first_name,
            last_name=informacion.last_name,
            country=informacion.country,
            email=informacion.email,
            birthdate=informacion.birthdate
        )
