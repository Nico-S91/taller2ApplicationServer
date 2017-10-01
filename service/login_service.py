""" @package login_service
"""

class LoginService:
    """Esta clase tiene la informacion que maneja el login y el logout de los clientes"""

    def __init__(self):
        #users por el momento solo aceptamos esto, despues vamos a usar la info de la base
        self.user_data = {
            "admin": "password",
            "ricveal": "1234"
        }

    def is_logged(self, session):
        """Verifica si esta logueado el usuario o no lo esta"""
        if 'username' in session:
            return True
        return False

    def login(self, username, password, session):
        """Login del cliente"""
        if self.user_data.get(username) == password:
            session['username'] = username
            return True
        return False

    def login_facebook(self, facebook_auth_token, session):
        """Login del cliente con el token de facebook"""
        if self.user_data.get(facebook_auth_token):
            username = facebook_auth_token
            session['username'] = username
            return True
        return False

    def logout(self, session):
        """Logout del cliente"""
        session.pop('username', None)
