""" @package model.client_shared
"""
import json
from flask import jsonify

def get_json_client_credentials(username, password):
    """ Devuelve el json que tenemos que enviarle al SharedServer para validar credenciales
        a partir del username y el password
        @param username es el nombre del usuario
        @param password es la contrasenia del usuario
    """
    data = {}
    data['username'] = username
    data['password'] = password
    return data

def get_json_client_credentials_facebook(facebook_auth_token):
    """ Devuelve el json que tenemos que enviarle al SharedServer para validar credenciales
        a partir del token de facebook
        @param facebook_auth_token es el token de facebook del cliente
    """
    data = {}
    data['facebookAuthToken'] = facebook_auth_token
    return data

class ClientShared:
    """Esta clase tiene la informacion que maneja el shared server para los clientes
    (los clientes del shared server son los clientes de la api y los choferes)
    """
    def __init__(self):
        """The constructor."""
        self.client_id = ""
        self.ref = ""
        self.type_client = ""
        self.username = ""
        self.password = ""
        self.fb_user_id = ""
        self.fb_auth_token = ""
        self.first_name = ""
        self.last_name = ""
        self.country = ""
        self.email = ""
        self.birthdate = ""
        self.images = []

    @staticmethod
    def new_client(ref, type_client, username, password, fb_user_id, fb_auth_token,
                   first_name, last_name, country, email, birthdate):
        """ Constructor con la informacion necesaria para crear o modificar un cliente
            @param ref es la referencia del cliente
            @param type_client es el tipo de cliente
            @param username es el nombre de usuario
            @param password es la contrasenia del usuario
            @param fb_user_id es la cuenta de facebook
            @param fb_auth_token es el token del usuario del facebook
            @param first_name es el nombre del cliente
            @param last_name es el apellido del cliente
            @param country es el pais del origen del cliente
            @param email es el mail del cliente
            @param birthdate es la fecha de nacimiento del cliente"""
        client = ClientShared()
        client.ref = ref
        client.type_client = type_client
        client.username = username
        client.password = password
        client.fb_user_id = fb_user_id
        client.fb_auth_token = fb_auth_token
        client.first_name = first_name
        client.last_name = last_name
        client.country = country
        client.email = email
        client.birthdate = birthdate
        return client

    @staticmethod
    def new_client_json(json_client, type_client):
        """ Constructor para agregar la informacion de un cliente que viene en el json
            @param json_client es el json con la informacion del cliente
            @param type_client es el tipo de cliente"""
        client = ClientShared()
        client.ref = 1
        client.type_client = type_client
        client.username = json_client["username"]
        client.password = json_client["password"]
        client.fb_user_id = json_client["fb"]["userId"]
        client.fb_auth_token = json_client["fb"]["authToken"]
        client.first_name = json_client["firstName"]
        client.last_name = json_client["lastName"]
        client.country = json_client["country"]
        client.email = json_client["email"]
        client.birthdate = json_client["birthdate"]
        #Falta agregar las imagenes
        return client

    def add_image(self, imagen):
        """ Agregar una imagen al usuario del cliente
            @param imagen es la imagen del cliente que se quiere agregar
        """
        self.images.append(imagen)

    def get_json_new_client(self):
        """ Json con la informacion del cliente que necesita el Shared para crear
            el cliente
        """
        return jsonify(
            _ref=self.ref,
            type_client=self.type_client,
            username=self.username,
            password=self.password,
            fb_user_id=self.fb_user_id,
            fb_auth_token=self.fb_auth_token,
            first_name=self.first_name,
            last_name=self.last_name,
            country=self.country,
            email=self.email,
            birthdate=self.birthdate
        )
