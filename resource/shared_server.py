""" @package shared_server
"""
import http
from model import client_shared
from model.client_shared import ClientShared
from flask import jsonify
import http, urllib
import json
import requests

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
#    abrir_conexion = httplib.HTTPConnection(URL_SHARED_SERVER)

#   def peticion(self):
        #Parametros que hay que enviar
#        parametros = urllib.urlencode({'campo1': 'valor uno','campo2':'valor2'})
        #Hacemos la llamada
#        abrir_conexion.request("POST", "/archivo_cualquiera.php", parametros, cabeceras)
#        respuesta = abrir_conexion.getresponse()
        
        #Cerramos la coneccion
#        abrir_conexion.close()
#       return respuesta

    def __init__(self):
        SharedServer.url_shared_server = 'https://stormy-lowlands-30400.herokuapp.com'
        self.cabeceras = {"Content-type": "application/json"}
        #Por el momento tenemos aca los usuarios
        self.user_data = {
            "admin": "password",
            "ricveal": "1234"
        }

    def change_url(self, url_value):
        """ Modifica  el parametro url de la clase
        """
        SharedServer.url_shared_server = url_value

    def get_url(self, endpoint):
        """Devuelve la url formada para pegarle al shared server
        @param endpoint es el endpoint del shared server al que se le va a pegar"""
        return SharedServer.url_shared_server + endpoint + '?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImxsZXZhbWUiLCJpYXQiOjE1MDczODkxODQsImV4cCI6MTUwOTk4MTE4NH0.KGdbsCbiYQMXXhtuogpKX6FslNTRIg9wVadI_F-w5Ko'

    def get_validate_client(self, username, password):
        """Validamos que el usuario exista en el sistema
        @param username es el nombre del usuario que guardo en el sistema
        @param password es la contraseña del usuario"""
        credential = client_shared.get_json_client_credentials(username, password)

        url = self.get_url('/api/v1/users/validate')
        response_server = requests.post(url, json=credential)
        json_data = json.loads(response_server.text)

        if response_server.status_code == 200:
            response = jsonify(json_data)
            response.status_code = 200
        else:
            response = jsonify(code=1, message='Ese cliente no existe')
            response.status_code = 401
        return response

    def get_validate_client_facebook(self, facebook_auth_token):
        """Validamos que el usuario exista en el sistema
        @param facebookAuthToken es el token de facebook que tenemos guardado en el sistema"""
        credential = client_shared.get_json_client_credentials_facebook(facebook_auth_token)

        url = self.get_url('/api/v1/users/validate')
        response_server = requests.post(url, json=credential)
        json_data = json.loads(response_server.text)

        if response_server.status_code == 200:
            response = jsonify(json_data)
            response.status_code = 200
        else:
            response = jsonify(code=1, message='Ese cliente no existe')
            response.status_code = 401
        return response

    def put_client(self, client_id, client):
        """ Modifica la informacion de un cliente/chofer
            @param client es la informacion modificada del cliente/chofer existente
        """
        #Aca va a ir el codigo para hacer el pedido de modificacion del cliente/chofer
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
        #Abrimos conexion
        abrir_conexion = http.client.HTTPConnection(SharedServer.url_shared_server)

        #Hacemos la llamada
        abrir_conexion.request("GET", "/api/v1/driver/" + str(driver_id))
        response = abrir_conexion.getresponse()

        decode_msg = response.read().decode('utf-8')
        json_obj = json.loads(decode_msg)

        #Cerramos Conexion
        abrir_conexion.close()

        return json_obj

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
        response = jsonify({'list': lista})
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
