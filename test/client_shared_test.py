""" @package test.client_shared_test
"""
import unittest
from api import app

class TestClientController(unittest.TestCase):
    """Esta clase tiene los test de los endpoint del controller_client
    """
    def setUp(self):
        # creates a test client
        self.app = app.app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_home_status_code(self):

        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        print(str(result.data))
        self.assertEqual(result.data, b'{\n  "message": "hello world"\n}\n')

    def test(self):
        response = self.app.get('/api/v1/clientedefault')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{\n  "_ref": 1, \n  "birthdate": "21/01/2000", \n  "country": "Argentina", \n  "email": "pepe@gmail.com", \n  "fb_auth_token": "fb_auth_token", \n  "fb_user_id": "fb_user_id", \n  "first_name": "pepe", \n  "last_name": "lopez", \n  "password": "password", \n  "type_client": "cliente", \n  "username": "pepelopez"\n}\n')

## Solo lo dejo para que quede como ejemplo ##

#    def test_upper(self):
#        self.assertEqual('foo'.upper(), 'FOO')

#   def test_isupper(self):
#       self.assertTrue('FOO'.isupper())
#       self.assertFalse('Foo'.isupper())

#    def test_split(self):
#        s = 'hello world'
#        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
#        with self.assertRaises(TypeError):
#            s.split(2)
