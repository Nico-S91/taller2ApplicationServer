""" @package shared_server
"""
import http, urllib
import json
import requests
from model import client_shared
from model.client_shared import ClientShared
from model.car_shared import CarShared
from flask import jsonify

class SharedServer:
    """Conexion con el Shared server"""

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

    def get_token(self):
        """ Devuelve el token para usar el shared server
        """
        return 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImxsZXZhbWUiLCJpYXQiOjE1MDczODkxODQsImV4cCI6MTUwOTk4MTE4NH0.KGdbsCbiYQMXXhtuogpKX6FslNTRIg9wVadI_F-w5Ko'

    def get_url(self, endpoint):
        """Devuelve la url formada para pegarle al shared server
        @param endpoint es el endpoint del shared server al que se le va a pegar"""
        return SharedServer.url_shared_server + endpoint + '?token=' + self.get_token()

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
        url = self.get_url('/api/v1/users/'+str(client_id))
        response_server = requests.put(url, json=client)
        return response_server

    def post_client(self, client):
        """ Crea un nuevo cliente/chofer
            @param client es la informacion del cliente/chofer
        """
        url = self.get_url('/api/v1/users')
        response_server = requests.post(url, json=client)
        return response_server

    def get_client(self, client_id):
        """ Devuelve la informacion del cliente buscado
            @param client_id es el id del cliente buscado
        """
        #Aca va a ir el codigo para hacer el pedido de get del cliente/chofer
        url = self.get_url('/api/v1/users/'+str(client_id))
        response_server = requests.get(url)
        # json_data = json.loads(response_server.text)
        return response_server

    def get_clients(self, type_client):
        """ Devuelve la informacion del cliente/chofer buscado
            @param client_id es el id del cliente/chofer buscado
        """
        url = self.get_url('/api/v1/users')
        response_server = requests.get(url)
        return response_server

    def delete_client(self, client_id):
        """ Elimina un cliente/chofer
            @param client_id es el id del cliente/chofer que se desea eliminar
        """
        #Aca va a ir el codigo para hacer el pedido de delete del cliente/chofer
        url = self.get_url('/api/v1/users/'+str(client_id))
        response_server = requests.delete(url)
        return response_server

    # Metodos para manipular autos

    def get_car(self, id_car, owner):
        """ Devuelve la informacion del auto de un cliente
            @param id_car es el id del auto del cliente
            @param owner es el id del cliente buscado
        """
        #Aca va a ir el codigo para hacer el pedido de get del auto del cliente
        metadata = {
                "version": "1"
            }
        car = {
            "id": "1",
            "_ref": "dfsd",
            "owner": "23",
            "properties": [
            {
                "name": "color",
                "value": "negro"
            },
            {
                "name": "modelo",
                "value": "punto"
            },
            {
                "name": "marca",
                "value": "fiat"
            }
            ]
        }
        response = jsonify({'metadata': metadata, 'car': car})
        response.status_code = 200
        return response

    def post_car(self, properties, client_id):
        """ Crea un nuevo auto para el chofer
            @param properties son las propiedades del auto del chofer
            @param client_id es el identificador del chofer
        """
        #Aca va a ir el codigo para hacer el pedido de crear un cliente/chofer
        response = self.get_car(45, client_id)
        response.status_code = 201
        return response

    def put_car(self, propertiesjson, car_id, client_id):
        """ Modifica el auto de un chofer
            @param properties son las propiedades del auto del chofer
            @param car_id es el identificador del auto
            @param client_id es el identificador del chofer
        """
        #Aca va a ir el codigo para hacer el pedido de crear un cliente/chofer
        response = self.get_car(45, client_id)
        response.status_code = 201
        return response

    def delete_car(self, driver_id, car_id):
        """ Este metodo permite eliminar un auto de un chofer
            @param car_id identificadore del auto
            @param driver_id identificador del conductor"""
            #Aca va a ir el codigo para hacer el pedido de delete del auto de un chofer
        response = jsonify('')
        response.status_code = 204
        return response
