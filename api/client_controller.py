""" @package api
"""
from model.client_shared import ClientShared

class ClientController:
    """Esta clase tiene los metodos para manajar la informacion de los clientes"""

    def __init__(self):
        """The constructor."""
        self.ref = ""

    def get_info_new_client(self):
        """ Este metodo solo sirve para las pruebas
            @param self es la informacion del cliente para armar el json"""
        client = ClientShared.new_client(1, "cliente", "Khaleesi", "Dragones3", "fb_user_id",
                                         "fb_auth_token", "Daenerys", "Targaryen", "Valyria",
                                         "madre_dragones@got.com", "01/01/1990")
        response = client.get_json_new_client()
        response.status_code = 200
        return response
