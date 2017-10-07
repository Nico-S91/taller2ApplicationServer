""" @package test.client_shared_test
"""
import unittest
import json
import main_app
import requests
from mock import MagicMock
from resource.shared_server import SharedServer

class TestClientController(unittest.TestCase):
    """Esta clase tiene los test de los endpoint del controller_client
    """
    def setUp(self):
        # creates a test client
        self.app = main_app.application.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_home_status_code(self):
        """Prueba el endpoint HelloWordl"""
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        print(str(result.data))
        self.assertEqual(result.data, b'{\n  "message": "hello world"\n}\n')

    #Pruebas de chofer

    def test_obtener_chofer_default(self):
        """Prueba de obtencion de chofer default"""
        response = self.app.get('/api/v1/driverdefault')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{\n  "_ref": 1, \n  "birthdate": "01/01/1990", \n  "country": "Valyria", \n  "email": "madre_dragones@got.com", \n  "fb_auth_token": "fb_auth_token", \n  "fb_user_id": "fb_user_id", \n  "first_name": "Daenerys", \n  "last_name": "Targaryen", \n  "password": "Dragones3", \n  "type_client": "chofer", \n  "username": "Khaleesi"\n}\n')

    def test_obtener_chofer(self):
        """Prueba que al obtener un chofer este sea igual al que viene por defecto"""
        # response = self.app.get('/api/v1/driver/23')
        response = requests.get('http://demo4909478.mockable.io/api/v1/driver/23')

        assert_res = json.loads("""
            {
                "username": "Khaleesi",
                "first_name": "Daenerys",
                "last_name": "Targaryen",
                "country": "Valyria",
                "fb_user_id": "fb_user_id",
                "birthdate": "01/01/1990",
                "type_client": "chofer",
                "fb_auth_token": "fb_auth_token",
                "client_id": 23,
                "email": "madre_dragones@got.com"
            }
        """)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json() == assert_res)

    def test_obtener_choferes(self):
        """Prueba que al obtener todos los choferes, viene el default"""
        response = requests.get('https://demo4909478.mockable.io/api/v1/drivers')
        assert_res = json.loads("""
                {
            "list": [
                {
                    "birthdate": "08/04/2005",
                    "client_id": 15,
                    "country": "Winterfell",
                    "email": "chica_sin_cara@got.com",
                    "fb_auth_token": "fb_auth_token",
                    "fb_user_id": "fb_user_id",
                    "first_name": "Arya",
                    "last_name": "Stark",
                    "type_client": "chofer",
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
                    "type_client": "chofer",
                    "username": "Khaleesi"
                }
            ]
        }""")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json() == assert_res)

    def test_crear_chofer(self):
        """Prueba que al crear un chofer con la informacion valida entonces devuelva
           un mensaje que se creo correctamente"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.post(
            '/api/v1/driver', data=payload, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data, b'{\n  "codigo": 0, \n  "mensaje": "El cliente fue creado correctamente"\n}\n')

    def test_crear_chofer_sin_informacion(self):
        """Prueba que al crear un chofer sin mandar la informacion devuelva el codigo de
           error correspondiente"""
        payload = ''
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.post(
            '/api/v1/driver', data=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_modificar_chofer(self):
        """Prueba que al modificar un chofer con la informacion valida entonces devuelve
           un mensaje que se creo correctamente"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put(
            '/api/v1/driver/88', data=payload, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data, b'{\n  "codigo": 0, \n  "mensaje": "El cliente fue modificado correctamente"\n}\n')

    def test_modificar_chofer_sin_informacion(self):
        """Prueba que al modificar un chofer sin mandar la informacion devuelva el codigo de
           error correspondiente"""
        payload = ''
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put(
            '/api/v1/driver/14', data=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_eliminar_chofer(self):
        """Prueba eliminar un chofer"""
        response = self.app.delete('/api/v1/driver/45')
        self.assertEqual(response.status_code, 204)

    #Pruebas de cliente

    def test_obtener_cliente_default(self):
        """Prueba que al obtener un cliente sea el que viene por defecto"""
        response = self.app.get('/api/v1/clientedefault')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{\n  "_ref": 1, \n  "birthdate": "01/01/1990", \n  "country": "Valyria", \n  "email": "madre_dragones@got.com", \n  "fb_auth_token": "fb_auth_token", \n  "fb_user_id": "fb_user_id", \n  "first_name": "Daenerys", \n  "last_name": "Targaryen", \n  "password": "Dragones3", \n  "type_client": "cliente", \n  "username": "Khaleesi"\n}\n')

    def test_obtener_cliente(self):
        """Prueba que al obtener un cliente sea el que viene por defecto"""
        response = self.app.get('/api/v1/client/23')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{\n  "birthdate": "01/01/1990", \n  "client_id": 23, \n  "country": "Valyria", \n  "email": "madre_dragones@got.com", \n  "fb_auth_token": "fb_auth_token", \n  "fb_user_id": "fb_user_id", \n  "first_name": "Daenerys", \n  "last_name": "Targaryen", \n  "type_client": "cliente", \n  "username": "Khaleesi"\n}\n')

    def test_obtener_clientes(self):
        """Prueba que al obtener todos los cliente que viene por defecto"""
        response = self.app.get('/api/v1/clients')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{\n  "list": [\n    {\n      "birthdate": "08/04/2005", \n      "client_id": 15, \n      "country": "Winterfell", \n      "email": "chica_sin_cara@got.com", \n      "fb_auth_token": "fb_auth_token", \n      "fb_user_id": "fb_user_id", \n      "first_name": "Arya", \n      "last_name": "Stark", \n      "type_client": "cliente", \n      "username": "ChicaSinRostro"\n    }, \n    {\n      "birthdate": "01/01/1990", \n      "client_id": 15, \n      "country": "Valyria", \n      "email": "madre_dragones@got.com", \n      "fb_auth_token": "fb_auth_token", \n      "fb_user_id": "fb_user_id", \n      "first_name": "Daenerys", \n      "last_name": "Targaryen", \n      "type_client": "cliente", \n      "username": "Khaleesi"\n    }\n  ]\n}\n')

    def test_crear_cliente(self):
        """Prueba que al crear un cliente con la informacion valida entonces devuelva
           un mensaje que se creo correctamente"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.post(
            '/api/v1/client', data=payload, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data, b'{\n  "codigo": 0, \n  "mensaje": "El cliente fue creado correctamente"\n}\n')

    def test_crear_cliente_sin_informacion(self):
        """Prueba que al crear un cliente sin mandar la informacion tire el codigo de
           error correspondiente"""
        payload = ''
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.post(
            '/api/v1/client', data=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_modificar_cliente(self):
        """Prueba que al modificar un cliente con la informacion valida entonces devuelva
           un mensaje que se creo correctamente"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put(
            '/api/v1/client/22', data=payload, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data, b'{\n  "codigo": 0, \n  "mensaje": "El cliente fue modificado correctamente"\n}\n')

    def test_modificar_cliente_sin_informacion(self):
        """Prueba que al modificar un cliente sin mandar la informacion tire el codigo de
           error correspondiente"""
        payload = ''
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put(
            '/api/v1/client/22', data=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_eliminar_cliente(self):
        """Prueba eliminar un cliente"""
        response = self.app.delete('/api/v1/client/23')
        self.assertEqual(response.status_code, 204)

## Test con Mocks
    def test_obtener_lista_choferes(self):
        cmp_test = json.loads("""{
        "list": [
            {
            "birthdate": "08/04/2005",
            "client_id": 15,
            "country": "Winterfell",
            "email": "chica_sin_cara@got.com",
            "fb_auth_token": "fb_auth_token",
            "fb_user_id": "fb_user_id",
            "first_name": "Arya",
            "last_name": "Stark",
            "type_client": "chofer",
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
            "type_client": "chofer",
            "username": "Khaleesi"
            }
        ]
        }""")

        SharedServer.URL_SHARED_SERVER = MagicMock(return_value='demo4909478.mockable.io')
        response = self.app.get('/api/v1/drivers')
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(cmp_response == cmp_test)


    def test_mock_obtener_chofer(self):
        cmp_test = json.loads("""{
            "birthdate": "01/01/1990",
            "client_id": 23,
            "country": "Valyria",
            "email": "madre_dragones@got.com",
            "fb_auth_token": "fb_auth_token",
            "fb_user_id": "fb_user_id",
            "first_name": "Daenerys",
            "last_name": "Targaryen",
            "type_client": "chofer",
            "username": "Khaleesi"
        }""")

        # mock_url = MagicMock(return_value='demo4909478.mockable.io')
        SharedServer.change_url(SharedServer, 'demo4909478.mockable.io')
        response = self.app.get('/api/v1/driver/23')
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(cmp_response == cmp_test)
