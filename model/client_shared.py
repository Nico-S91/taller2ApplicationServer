""" @package model.client_shared
"""

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
