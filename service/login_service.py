""" @package login_service
"""
from resource.shared_server import SharedServer

SHARED_SERVER = SharedServer()

class LoginService:
    """Esta clase tiene la informacion que maneja el login y el logout de los clientes"""

    def is_logged(self, session):
        """Verifica si esta logueado el usuario o no lo esta
        @param session es la sesion del usuario"""
        if 'username' in session:
            return True
        print('False')
        return False

    def login(self, username, password, session):
        """Logueamos al usuario
        @param username es el nombre del usuario que guardo en el sistema
        @param password es la contraseña del usuario
        @param session es la sesion del usuario"""
        if SHARED_SERVER.get_validate_client(username, password):
            session['username'] = username
            return True
        return False

    def login_facebook(self, facebook_auth_token, session):
        """Logueamos al usuario
        @param facebookAuthToken es el token de facebook que tenemos guardado en el sistema
        @param session es la sesion del usuario"""
        if SHARED_SERVER.get_validate_client_facebook(facebook_auth_token):
            session['username'] = facebook_auth_token
            return True
        return False

    def logout(self, session):
        """Logout del cliente
        @param session es la sesion del usuario"""
        session.pop('username', None)
        return session
