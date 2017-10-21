""" @package test.transaction_controller_test
"""
import unittest
import json
from test.response_mock import ResponseMock
from service.shared_server import SharedServer
from mock import MagicMock
from service.login_service import LoginService
import main_app

class TestTransactionController(unittest.TestCase):
    """Esta clase tiene los test de los endpoint del trip_controller
    """

    def setUp(self):
        # creates a test client
        self.app = main_app.application.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True
        SharedServer._get_token_initial = MagicMock(return_value='')
        SharedServer._refresh_token = MagicMock(return_value='')

    def mockeamos_login_correcto(self):
        """Mockeamos para que el login de correcto"""
        LoginService.is_logged = MagicMock(return_value=SharedServer)

    # GET medios de pagos

    def test_obtener_metodos_pago(self):
        """Prueba que al obtener los metodos de pagos que acepta el sistema"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'count': 0,
                'total': 0,
                'next': 'string',
                'prev': 'string',
                'first': 'string',
                'last': 'string',
                'version': 'string'
            },
            'paymethods': [
                {
                    'name': 'tarjeta',
                    'parameters': [
                        {
                            'type':'habitual'
                        }
                    ]
                }
            ]
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_payment_methods = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/paymentmethods')
        print(response)
        assert_res = json.loads("""
        [
            {
                "name": "tarjeta",
                "parameters": [
                    {"type": "habitual"}
                ]
            }
        ]""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_metodos_pago_sin_autorizacion(self):
        """Prueba que al obtener los metodos de pagos que acepta el sistema sin autorizacion"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': '0',
            'message': 'Ups...no tiene autorizacion'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(401)
        SharedServer.get_payment_methods = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/paymentmethods')
        print(response)
        assert_res = json.loads("""
        {
            "code": "0",
            "message": "Ups...no tiene autorizacion"
        }""")
        self.assertEqual(response.status_code, 401)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    #GET transacciones de clientes

    def test_informacion_transacciones_cliente(self):
        """Prueba que al obtener las transacciones de un cliente"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'count': 2,
                'total': 2,
                'next': 'string',
                'prev': 'string',
                'first': 'string',
                'last': 'string',
                'version': 'xx'
            },
            'transactions': [
                {
                    'id': '1',
                    'trip': '1',
                    'timestamp': 0,
                    'cost': {
                        'currency': 'pesos',
                        'value': 100
                    },
                    'description': 'Es que me hizo esperar mucho',
                    'data': {}
                },
                {
                    'id': '1',
                    'trip': '1',
                    'timestamp': 0,
                    'cost': {
                        'currency': 'pesos',
                        'value': 48
                    },
                    'description': 'Nada para acotar',
                    'data': {}
                }
            ]
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_transactions = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/client/23/transactions')
        assert_res = json.loads("""
        [
            {
            "id": "1",
            "trip": "1",
            "timestamp": 0,
            "cost": {
                "currency": "pesos",
                "value": 100
            },
            "description": "Es que me hizo esperar mucho",
            "data": {}
            },
            {
            "id": "1",
            "trip": "1",
            "timestamp": 0,
            "cost": {
                "currency": "pesos",
                "value": 48
            },
            "description": "Nada para acotar",
            "data": {}
            }
        ]""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_transacciones_cliente_sin_autorizacion(self):
        """Prueba que al obtener la informacion de las transacciones de un cliente sin autorizacion"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': '0',
            'message': 'Ups...no tiene autorizacion'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(401)
        SharedServer.get_transactions = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/client/8/transactions')
        assert_res = json.loads("""
        {
            "code": "0",
            "message": "Ups...no tiene autorizacion"
        }""")
        self.assertEqual(response.status_code, 401)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    #GET transacciones de choferes

    def test_informacion_transacciones_chofer(self):
        """Prueba que al obtener las transacciones de un chofer"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'count': 2,
                'total': 2,
                'next': 'string',
                'prev': 'string',
                'first': 'string',
                'last': 'string',
                'version': 'xx'
            },
            'transactions': [
                {
                    'id': '1',
                    'trip': '1',
                    'timestamp': 0,
                    'cost': {
                        'currency': 'pesos',
                        'value': 150
                    },
                    'description': 'Es que me hizo esperar mucho',
                    'data': {}
                },
                {
                    'id': '1',
                    'trip': '1',
                    'timestamp': 0,
                    'cost': {
                        'currency': 'dolares',
                        'value': 48
                    },
                    'description': 'Nada para acotar',
                    'data': {}
                }
            ]
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_transactions = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/driver/23/transactions')
        assert_res = json.loads("""
        [
            {
            "id": "1",
            "trip": "1",
            "timestamp": 0,
            "cost": {
                "currency": "pesos",
                "value": 150
            },
            "description": "Es que me hizo esperar mucho",
            "data": {}
            },
            {
            "id": "1",
            "trip": "1",
            "timestamp": 0,
            "cost": {
                "currency": "dolares",
                "value": 48
            },
            "description": "Nada para acotar",
            "data": {}
            }
        ]""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_transacciones_chofer_sin_autorizacion(self):
        """Prueba que al obtener la informacion de las transacciones de un
            chofer sin autorizacion"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': '0',
            'message': 'Ups...no tiene autorizacion'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(401)
        SharedServer.get_transactions = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/driver/8/transactions')
        assert_res = json.loads("""
        {
            "code": "0",
            "message": "Ups...no tiene autorizacion"
        }""")
        self.assertEqual(response.status_code, 401)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    # POST de las transacciones de los clientes

    def test_guardar_transaccion(self):
        """Prueba guardar una transaccion"""
        self.mockeamos_login_correcto()
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'XX'
            },
            'transaction': {
                'id': 'carlitos',
                'trip': '1',
                'timestamp': 123333000,
                'cost': {
                    'currency': 'pesos',
                    'value': 100
                },
                'description': 'Algo...',
                'data': {}
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        SharedServer.post_transactions = MagicMock(return_value=response_mock)
        response = self.app.post('/api/v1/client/23/transactions', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "id": "carlitos",
            "trip": "1",
            "timestamp": 123333000,
            "cost": {
                "currency": "pesos",
                "value": 100
            },
            "description": "Algo...",
            "data": {}
        }""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_guardar_transaccion_sin_autorizacion(self):
        """Prueba guardar una transaccion sin autorizacion"""
        self.mockeamos_login_correcto()
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 2,
            'message': 'No esta autorizado'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(401)
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        SharedServer.post_transactions = MagicMock(return_value=response_mock)
        response = self.app.post('/api/v1/client/8/transactions', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 2,
            "message": "No esta autorizado"
        }""")
        self.assertEqual(response.status_code, 401)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    # POST de las transacciones de los choferes

    def test_guardar_transaccion_chofer(self):
        """Prueba guardar una transaccion de un chofer"""
        self.mockeamos_login_correcto()
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'XX'
            },
            'transaction': {
                'id': 'claudia',
                'trip': '1',
                'timestamp': 123333000,
                'cost': {
                    'currency': 'pesos',
                    'value': 65
                },
                'description': 'Algo...no se',
                'data': {}
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        SharedServer.post_transactions = MagicMock(return_value=response_mock)
        response = self.app.post('/api/v1/driver/23/transactions', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "id": "claudia",
            "trip": "1",
            "timestamp": 123333000,
            "cost": {
                "currency": "pesos",
                "value": 65
            },
            "description": "Algo...no se",
            "data": {}
        }""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_guardar_transaccion_sin_autorizacion_chofer(self):
        """Prueba guardar una transaccion sin autorizacion de un chofer"""
        self.mockeamos_login_correcto()
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 2,
            'message': 'No esta autorizado'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(401)
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        SharedServer.post_transactions = MagicMock(return_value=response_mock)
        response = self.app.post('/api/v1/driver/8/transactions', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 2,
            "message": "No esta autorizado"
        }""")
        self.assertEqual(response.status_code, 401)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
