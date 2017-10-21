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
