""" @package service.shared_server
"""
import json
import requests
from model import client_shared
from flask import jsonify

TIPO_CLIENTE = "passenger"
TIPO_CHOFER = "driver"

class SharedServer:
    """Conexion con el Shared server"""

    def __init__(self):
        self.url_shared_server = 'https://stormy-lowlands-30400.herokuapp.com'
        self.token = self._get_token_initial()

    def get_validate_client(self, username, password):
        """Validamos que el usuario exista en el sistema
        @param username es el nombre del usuario que guardo en el sistema
        @param password es la contrasenia del usuario"""
        credential = client_shared.get_json_client_credentials(username, password)
        return self._get_validate_client(credential)

    def get_validate_client_facebook(self, facebook_auth_token):
        """Validamos que el usuario exista en el sistema
        @param facebookAuthToken es el token de facebook que tenemos guardado en el sistema"""
        credential = client_shared.get_json_client_credentials_facebook(facebook_auth_token)
        return self._get_validate_client(credential)

    def put_client(self, client_id, client):
        """ Modifica la informacion de un cliente/chofer
            @param client es la informacion modificada del cliente/chofer existente
        """
        return self._put_shared_server('/api/v1/users/'+str(client_id), client)

    def post_client(self, client):
        """ Crea un nuevo cliente/chofer
            @param client es la informacion del cliente/chofer
        """
        return self._post_shared_server('/api/v1/users', client)

    def get_client(self, client_id):
        """ Devuelve la informacion del cliente buscado
            @param client_id es el id del cliente buscado
        """
        return self._get_shared_server('/api/v1/users/'+str(client_id))

    def get_clients(self):
        """ Devuelve la informacion de los clientes/choferes
        """
        return self._get_shared_server('/api/v1/users')

    def delete_client(self, client_id):
        """ Elimina un cliente/chofer
            @param client_id es el id del cliente/chofer que se desea eliminar
        """
        return self._delete_shared_server('/api/v1/users/'+str(client_id))

    # Metodos para manipular autos

    def get_car(self, id_car, owner):
        """ Devuelve la informacion del auto de un cliente
            @param id_car es el id del auto del cliente
            @param owner es el id del cliente buscado
        """
        return self._get_shared_server('/api/v1/users/'+str(owner)+'/cars/'+str(id_car))

    def get_cars(self, owner):
        """ Devuelve la informacion de los autos de un cliente
            @param owner es el id del cliente buscado
        """
        return self._get_shared_server('/api/v1/users/'+str(owner)+'/cars')

    def post_car(self, car, driver_id):
        """ Crea un nuevo auto para el chofer
            @param car son las propiedades del auto del chofer
            @param driver_id es el identificador del chofer
        """
        return self._post_shared_server('/api/v1/users/' + str(driver_id) + '/cars', car)

    def put_car(self, car, car_id, driver_id):
        """ Modifica el auto de un chofer
            @param car son las propiedades del auto del chofer
            @param car_id es el identificador del auto
            @param driver_id es el identificador del chofer
        """
        return self._put_shared_server('/api/v1/users/' + str(driver_id) + '/cars/'
                                       + str(car_id), car)

    def delete_car(self, driver_id, car_id):
        """ Este metodo permite eliminar un auto de un chofer
            @param car_id identificadore del auto
            @param driver_id identificador del conductor"""
        return self._delete_shared_server('/api/v1/users/' + str(driver_id) + '/cars/'
                                          + str(car_id))

    #Metodos para manipular viajes

    def get_payment_methods(self):
        """ Este metodo devuelve los metodos de pagos que acepta el Shared server
        """
        return self._get_shared_server('/api/v1/paymethods')

    def get_trip(self, trip_id):
        """ Este metodo devuelve la informacion de un viaje
            @param trip_id identificadore del viaje"""
        return self._get_shared_server('/api/v1/trips/' + str(trip_id))

    def post_trip_estimate(self, data):
        """ Calcula la estimacion de un viaje
            @param estimate informacion necesaria para estimar un viaje
        """
        return self._post_shared_server('/api/v1/trips/estimate', data)

    # Metodos privados

    def _get_token_initial(self):
        """ Devuelve el token inicial para usar el shared server
        """
        url = self.url_shared_server + '/api/v1/llevame'
        response_server = requests.get(url)
        json_data = json.loads(response_server.text)
        return json_data.get('token')

    def _refresh_token(self):
        """ Refresca el token para usar el shared server y damos seniales de vida
        """
        url = self._get_url('/api/v1/servers/ping')
        response_server = requests.post(url)
        json_data = json.loads(response_server.text)
        ping = json_data['ping']
        token = ping['token']
        self.token = token.get('token')

    def _get_url(self, endpoint):
        """Devuelve la url formada para pegarle al shared server
        @param endpoint es el endpoint del shared server al que se le va a pegar"""
        return self.url_shared_server + endpoint + '?token=' + self.token

    def _get_shared_server(self, endpoint):
        """Get al endpoint
        @param endpoint es el endpoint del shared server al que se le va a pegar"""
        self._refresh_token()
        url = self._get_url(endpoint)
        response_server = requests.get(url)
        return response_server

    def _post_shared_server(self, endpoint, json_data):
        """Post al endpoint
        @param endpoint es el endpoint del shared server al que se le va a pegar
        @param json_data es el json que se va a enviar en el post"""
        self._refresh_token()
        url = self._get_url(endpoint)
        response_server = requests.post(url, json=json_data)
        return response_server

    def _put_shared_server(self, endpoint, json_data):
        """Put al endpoint
        @param endpoint es el endpoint del shared server al que se le va a pegar
        @param json_data es el json que se va a enviar en el put"""
        self._refresh_token()
        url = self._get_url(endpoint)
        response_server = requests.put(url, json=json_data)
        return response_server

    def _delete_shared_server(self, endpoint):
        """Delete al endpoint
        @param endpoint es el endpoint del shared server al que se le va a pegar"""
        self._refresh_token()
        url = self._get_url(endpoint)
        response_server = requests.delete(url)
        return response_server

    def _get_validate_client(self, credential):
        """Validamos que el usuario a partir de las credenciales
        @param credential son las credenciales del usuario"""
        response_server = self._post_shared_server('/api/v1/users/validate', credential)
        json_data = json.loads(response_server.text)

        if response_server.status_code == 200:
            response = jsonify(json_data)
            response.status_code = 200
        else:
            response = jsonify(code=1, message='Ese cliente no existe')
            response.status_code = 401
        return response
