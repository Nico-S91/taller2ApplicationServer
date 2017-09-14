""" @package shared_server
"""
import json
from model.client_shared import ClientShared
from flask import jsonify

DEFAULT_CLIENT = ClientShared.new_client(1, "cliente", "Khaleesi", "Dragones3",
                                         "fb_user_id", "fb_auth_token", "Daenerys",
                                         "Targaryen", "Valyria", "madre_dragones@got.com",
                                         "01/01/1990")

DEFAULT_DRIVER = ClientShared.new_client(1, "chofer", "Khaleesi", "Dragones3",
                                         "fb_user_id", "fb_auth_token", "Daenerys",
                                         "Targaryen", "Valyria", "madre_dragones@got.com",
                                         "01/01/1990")

class SharedServer:
#    cabeceras = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    """Conexion con el Shared server"""
#    abrir_conexion = httplib.HTTPConnection("localhost:80")

#   def peticion(self):
        #Parametros que hay que enviar
#        parametros = urllib.urlencode({'campo1': 'valor uno','campo2':'valor2'})
        #Hacemos la llamada
#        abrir_conexion.request("POST", "/archivo_cualquiera.php", parametros, cabeceras)
#        respuesta = abrir_conexion.getresponse()
        #Imprime codigo de respuesta
#        print (respuesta.status)
        #Imprime el nombre del codigo de la respuesta
#        print (respuesta.reason)
#        ver_source = respuesta.read()
        #Cerramos la coneccion
#        abrir_conexion.close()

    def put_client(self, client_id, client):
        """ Modifica la informacion de un cliente/chofer
            @param client es la informacion modificada del cliente/chofer existente
        """
        #Aca va a ir el codigo para hacer el pedido de modificacion del cliente/chofer
        #Aca va a ir el codigo para hacer el pedido de crear un cliente/chofer

        if client.type_client == "cliente":
            response = DEFAULT_CLIENT.get_json_new_client()
            response.status_code = 201
        elif client.type_client == "chofer":
            response = DEFAULT_DRIVER.get_json_new_client()
            response.status_code = 201

        return response

    def post_client(self, client):
        """ Crea un nuevo cliente/chofer
            @param client es la informacion del cliente/chofer
        """
        #Aca va a ir el codigo para hacer el pedido de crear un cliente/chofer
        if client.type_client == "cliente":
            response = DEFAULT_CLIENT.get_json_new_client()
            response.status_code = 201
        elif client.type_client == "chofer":
            response = DEFAULT_DRIVER.get_json_new_client()
            response.status_code = 201

        return response

    def get_client(self, client_id):
        """ Devuelve la informacion del cliente buscado
            @param client_id es el id del cliente buscado
        """
        #Aca va a ir el codigo para hacer el pedido de get del cliente/chofer
        client = DEFAULT_CLIENT
        client.client_id = client_id

        return client

    def get_driver(self, driver_id):
        """ Devuelve la informacion del chofer buscado
            @param driver_id es el id del chofer buscado
        """
        #Aca va a ir el codigo para hacer el pedido de get del chofer
        client = DEFAULT_DRIVER
        client.client_id = driver_id

        return client

    def get_clients(self, type_client):
        """ Devuelve la informacion del cliente/chofer buscado
            @param client_id es el id del cliente/chofer buscado
        """
        #Aca va a ir el codigo para hacer el pedido de get de todos los cliente/chofer
#        lista_clients = []
#        client1 = DEFAULT_CLIENT
#        client1.client_id = 1
#        client1.type_client = type_client
#        client2 = DEFAULT_CLIENT
#        client2.client_id = 2
#        client2.type_client = type_client
#        lista_clients.append(client1)
#        lista_clients.append(client2)
#        response = json.dumps(lista_clients)
        lista = [
            {
                "birthdate": "08/04/2005",
                "client_id": 15,
                "country": "Winterfell",
                "email": "chica_sin_cara@got.com",
                "fb_auth_token": "fb_auth_token",
                "fb_user_id": "fb_user_id",
                "first_name": "Arya",
                "last_name": "Stark",
                "type_client": type_client,
                "username": "ChicaSinRostro"
            },
            {
                "birthdate": "01/01/1990",
                "client_id": 15,
                "country": "Valyria",
                "email": "madre_dragones@got.com",
                "fb_auth_token": "fb_auth_token",
                "fb_user_id": "fb_user_id",
                "first_name": "Daenerys",
                "last_name": "Targaryen",
                "type_client": type_client,
                "username": "Khaleesi"
            }
        ]
        response = jsonify({'tasks': lista})
        response.status_code = 200
        return response

    def delete_client(self, client_id):
        """ Elimina un cliente/chofer
            @param client_id es el id del cliente/chofer que se desea eliminar
        """
        #Aca va a ir el codigo para hacer el pedido de delete del cliente/chofer
        response = jsonify('')
        response.status_code = 204
        return response
