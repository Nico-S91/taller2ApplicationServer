import unittest
import mock
from resource.shared_server import SharedServer
from service.login_service import LoginService
import main_app

LOGIN_SERVICE = LoginService()

class TestLoginService(unittest.TestCase):
    """Esta clase tiene los test del login service
    """
    # def setUp(self):
    #     self.login_service = LoginService()

    # def test_login_correctamente(self):
    #     """"Se prueba que se haga el login correctamente"""
    #     SharedServer.get_validate_client = mock.MagicMock(return_value=True)
    #     username = 'user'
    #     password = 'pass'
    #     session = {}
    #     self.assertTrue(self.login_service.login(username, password, session))
    #     self.assertEqual(session['username'], username)

    # def test_login_facebook_correctamente(self):
    #     """"Se prueba que se haga el login correctamente"""
    #     SharedServer.get_validate_client = mock.MagicMock(return_value=True)
    #     facebook_auth_token = 'user'
    #     session = {}
    #     self.assertTrue(self.login_service.login_facebook(facebook_auth_token, session))
    #     self.assertEqual(session['username'], facebook_auth_token)

    # def test_login_incorrecto(self):
    #     """"Se prueba que se haga el login incorrecto"""
    #     SharedServer.get_validate_client = mock.MagicMock(return_value=False)
    #     username = 'user'
    #     password = 'pass'
    #     session = {}
    #     self.assertFalse(self.login_service.login(username, password, session))
    #     self.assertEqual(session, {})

    # def test_login_facebook_incorrecto(self):
    #     """"Se prueba que se haga el login incorrecto"""
    #     SharedServer.get_validate_client = mock.MagicMock(return_value=False)
    #     facebook_auth_token = 'user'
    #     session = {}
    #     self.assertFalse(self.login_service.login_facebook(facebook_auth_token, session))
    #     self.assertEqual(session, {})

    # def test_logout(self):
    #     """"Se prueba que se haga el logout"""
    #     session = {}
    #     session['username'] = 'user'
    #     print (session)
    #     session_logout = self.login_service.logout(session)
    #     self.assertEqual(session_logout, {})

    # def test_verificar_que_este_logueado(self):
    #     """"Se prueba que se verifique correctamente la session"""
    #     session = {}
    #     session['username'] = 'user'
    #     self.assertTrue(self.login_service.is_logged(session))

    # def test_verificar_que_no_este_logueado(self):
    #     """"Se prueba que se verifique correctamente que la session no este logueado"""
    #     session = {}
    #     self.assertFalse(self.login_service.is_logged(session))
