""" @package test.trip_controller_test
"""
import unittest
import json
from test.response_mock import ResponseMock
from service.shared_server import SharedServer
from mock import MagicMock
from service.login_service import LoginService
import main_app

class TestTripController(unittest.TestCase):
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
        
    #GET informacion de viaje de un cliente

    def test_informacion_viaje_cliente(self):
        """Prueba que al obtener la informacion de un viaje de un cliente"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'trip': {
                'id': '1',
                'applicationOwner': 'App',
                'driver': 'jose',
                'passenger': '23',
                'start': {
                    'address': {
                        'street': 'Calle falsa 123',
                        'location': {
                            'lat': -34.619996,
                            'lon': -58.686680
                        }
                    },
                    'timestamp': 1523377380000
                },
                'end': {
                    'address': {
                        'street': 'Cactus 852',
                        'location': {
                            'lat': -34.649372,
                            'lon': -58.617885
                        }
                    },
                    'timestamp': 1523378880000
                },
                'totalTime': 1500000,
                'waitTime': 20000,
                'travelTime': 0,
                'distance': 8,
                'route': [
                    {
                        'location': {
                            'lat': 0,
                            'lon': 0
                        },
                        'timestamp': 0
                    }
                ],
                'cost': {
                    'currency': 'tarjeta Violeta',
                    'value': 56
                }
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_trip = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/client/23/trips/1')
        print(response)
        assert_res = json.loads("""
        {
            "id": "1",
            "applicationOwner": "App",
            "driver": "jose",
            "passenger": "23",
            "start": {
                "address": {
                    "street": "Calle falsa 123",
                    "location": {
                        "lat": -34.619996,
                        "lon": -58.686680
                    }
                },
                "timestamp": 1523377380000
            },
            "end": {
                "address": {
                    "street": "Cactus 852",
                    "location": {
                        "lat": -34.649372,
                        "lon": -58.617885
                    }
                },
                "timestamp": 1523378880000
            },
            "totalTime": 1500000,
            "waitTime": 20000,
            "travelTime": 0,
            "distance": 8,
            "route": [
                {
                    "location": {
                        "lat": 0,
                        "lon": 0
                    },
                    "timestamp": 0
                }
            ],
            "cost": {
                "currency": "tarjeta Violeta",
                "value": 56
            }
        }""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_informacion_viaje_cliente_sin_autorizacion(self):
        """Prueba que al obtener la informacion de un viaje de un cliente sin autorizacion"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': '0',
            'message': 'Ups...no tiene autorizacion'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(401)
        SharedServer.get_trip = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/client/8/trips/1')
        print(response)
        assert_res = json.loads("""
        {
            "code": "0",
            "message": "Ups...no tiene autorizacion"
        }""")
        self.assertEqual(response.status_code, 401)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_informacion_cliente_viaje_que_no_existe(self):
        """Prueba que al obtener la informacion de un viaje de un cliente que no existe"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': '1',
            'message': 'No existe el viaje'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(404)
        SharedServer.get_trip = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/client/2/trips/888')
        print(response)
        assert_res = json.loads("""
        {
            "code": "1",
            "message": "No existe el viaje"
        }""")
        self.assertEqual(response.status_code, 404)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_informacion_cliente_viaje_de_otro_cliente(self):
        """Prueba que al obtener la informacion de un viaje de otro cliente"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'trip': {
                'id': '1',
                'applicationOwner': 'App',
                'driver': 'jose',
                'passenger': 'pepito',
                'start': {
                    'address': {
                        'street': 'Calle falsa 123',
                        'location': {
                            'lat': -34.619996,
                            'lon': -58.686680
                        }
                    },
                    'timestamp': 1523377380000
                },
                'end': {
                    'address': {
                        'street': 'Cactus 852',
                        'location': {
                            'lat': -34.649372,
                            'lon': -58.617885
                        }
                    },
                    'timestamp': 1523378880000
                },
                'totalTime': 1500000,
                'waitTime': 20000,
                'travelTime': 0,
                'distance': 8,
                'route': [
                    {
                        'location': {
                            'lat': 0,
                            'lon': 0
                        },
                        'timestamp': 0
                    }
                ],
                'cost': {
                    'currency': 'tarjeta Violeta',
                    'value': 56
                }
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_trip = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/client/2/trips/1')
        print(response)
        assert_res = json.loads("""
        {
            "code": -1,
            "message": "El viaje no pertenece al usuario"
        }""")
        self.assertEqual(response.status_code, 401)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    # GET informacion de un chofer

    def test_informacion_viaje_chofer(self):
        """Prueba que al obtener la informacion de un viaje de un chofer"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'trip': {
                'id': '1',
                'applicationOwner': 'App',
                'driver': '2',
                'passenger': 'pepito',
                'start': {
                    'address': {
                        'street': 'Calle falsa 123',
                        'location': {
                            'lat': -34.619996,
                            'lon': -58.686680
                        }
                    },
                    'timestamp': 1523377380000
                },
                'end': {
                    'address': {
                        'street': 'Cactus 852',
                        'location': {
                            'lat': -34.649372,
                            'lon': -58.617885
                        }
                    },
                    'timestamp': 1523378880000
                },
                'totalTime': 1500000,
                'waitTime': 20000,
                'travelTime': 0,
                'distance': 8,
                'route': [
                    {
                        'location': {
                            'lat': 0,
                            'lon': 0
                        },
                        'timestamp': 0
                    }
                ],
                'cost': {
                    'currency': 'tarjeta Violeta',
                    'value': 56
                }
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_trip = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/driver/2/trips/1')
        print(response)
        assert_res = json.loads("""
        {
            "id": "1",
            "applicationOwner": "App",
            "driver": "2",
            "passenger": "pepito",
            "start": {
                "address": {
                    "street": "Calle falsa 123",
                    "location": {
                        "lat": -34.619996,
                        "lon": -58.686680
                    }
                },
                "timestamp": 1523377380000
            },
            "end": {
                "address": {
                    "street": "Cactus 852",
                    "location": {
                        "lat": -34.649372,
                        "lon": -58.617885
                    }
                },
                "timestamp": 1523378880000
            },
            "totalTime": 1500000,
            "waitTime": 20000,
            "travelTime": 0,
            "distance": 8,
            "route": [
                {
                    "location": {
                        "lat": 0,
                        "lon": 0
                    },
                    "timestamp": 0
                }
            ],
            "cost": {
                "currency": "tarjeta Violeta",
                "value": 56
            }
        }""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_informacion_viaje_chofer_sin_autorizacion(self):
        """Prueba que al obtener la informacion de un viaje de un chofer sin autorizacion"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': '0',
            'message': 'Ups...no tiene autorizacion'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(401)
        SharedServer.get_trip = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/driver/8/trips/1')
        print(response)
        assert_res = json.loads("""
        {
            "code": "0",
            "message": "Ups...no tiene autorizacion"
        }""")
        self.assertEqual(response.status_code, 401)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_informacion_viaje_chofer_que_no_existe(self):
        """Prueba que al obtener la informacion de un viaje de un chofer que no existe"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': '1',
            'message': 'No existe el viaje'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(404)
        SharedServer.get_trip = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/driver/2/trips/888')
        print(response)
        assert_res = json.loads("""
        {
            "code": "1",
            "message": "No existe el viaje"
        }""")
        self.assertEqual(response.status_code, 404)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_informacion_chofer_viaje_de_otro_cliente(self):
        """Prueba que al obtener la informacion de un viaje de otro chofer"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'trip': {
                'id': '1',
                'applicationOwner': 'App',
                'driver': 'jose',
                'passenger': 'pepito',
                'start': {
                    'address': {
                        'street': 'Calle falsa 123',
                        'location': {
                            'lat': -34.619996,
                            'lon': -58.686680
                        }
                    },
                    'timestamp': 1523377380000
                },
                'end': {
                    'address': {
                        'street': 'Cactus 852',
                        'location': {
                            'lat': -34.649372,
                            'lon': -58.617885
                        }
                    },
                    'timestamp': 1523378880000
                },
                'totalTime': 1500000,
                'waitTime': 20000,
                'travelTime': 0,
                'distance': 8,
                'route': [
                    {
                        'location': {
                            'lat': 0,
                            'lon': 0
                        },
                        'timestamp': 0
                    }
                ],
                'cost': {
                    'currency': 'tarjeta Violeta',
                    'value': 56
                }
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_trip = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/driver/2/trips/1')
        print(response)
        assert_res = json.loads("""
        {
            "code": -1,
            "message": "El viaje no pertenece al usuario"
        }""")
        self.assertEqual(response.status_code, 401)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    # POST de la estimacion de un viaje

    def test_obtener_estimacion(self):
        """Prueba para estimar un viaje"""
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
                'version': '1'
            },
            'cost': {
                'currency': 'tarjeta Violeta',
                'value': 56
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(201)
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        SharedServer.post_trip_estimate = MagicMock(return_value=response_mock)
        response = self.app.post('/api/v1/trips/estimate', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "currency": "tarjeta Violeta",
            "value": 56
        }""")
        self.assertEqual(response.status_code, 201)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_estimar_con_insuficientes_parametros(self):
        """Prueba estimar valor de viaje con falta de informacion"""
        self.mockeamos_login_correcto()
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 1,
            'message': 'Incumplimiento de precondiciones'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(400)
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        SharedServer.post_trip_estimate = MagicMock(return_value=response_mock)
        response = self.app.post('/api/v1/trips/estimate', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 1,
            "message": "Incumplimiento de precondiciones"
        }""")
        self.assertEqual(response.status_code, 400)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_estimar_sin_autorizacion(self):
        """Prueba estimar valor de viaje sin autorizacion"""
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
        SharedServer.post_trip_estimate = MagicMock(return_value=response_mock)
        response = self.app.post('/api/v1/trips/estimate', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 2,
            "message": "No esta autorizado"
        }""")
        self.assertEqual(response.status_code, 401)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_estimar_con_problemas_pagos(self):
        """Prueba estimar valor de viaje con problemas de pagos"""
        self.mockeamos_login_correcto()
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 3,
            'message': 'El pasajero debe normalizar su situación de pago. No se le debe permitir realizar el pago.'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(402)
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        SharedServer.post_trip_estimate = MagicMock(return_value=response_mock)
        response = self.app.post('/api/v1/trips/estimate', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 3,
            "message": "El pasajero debe normalizar su situación de pago. No se le debe permitir realizar el pago."	

        }""")
        self.assertEqual(response.status_code, 402)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
