import unittest
import json
from model.client_shared import ClientShared

class TestStringMethods(unittest.TestCase):

    def test_json_para_crear_cliente(self):
        cliente = ClientShared.new_client(1, "cliente", "pepelopez", "password", "fb_user_id", "fb_auth_token", "pepe", "lopez", "Argentina", "pepe@gmail.com", "21/01/2000")
        response = json.loads(cliente.get_json_new_client())
        self.assertEqual(response, "")

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()