# coding=utf-8
""" @package test.trip_controller_test
"""
import unittest
import json
from test.response_mock import ResponseMock
from service.shared_server import SharedServer
from api.model_manager import ModelManager
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
        response_info_user = {
            'client_type': 'passenger'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = None
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
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

    def test_informacion_viaje_cliente_mongo(self):
        """Prueba que al obtener la informacion de un viaje que se encuentra en
        mongo"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_info_user = {
            'client_type': 'passenger'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = {
            'id': 1,
            'passenger_id': '23',
            'trip': 'Aca estaria toda la info...'
        }
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/client/23/trips/1')
        print(response)
        assert_res = json.loads("""
        {
            "id": 1,
            "passenger_id": "23",
            "trip": "Aca estaria toda la info..."
        }""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_informacion_viaje_cliente_mongo2(self):
        """Prueba que al obtener la informacion de un viaje que se encuentra en
        mongo y el usuario no estaba en mongo"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'user': {
                'id': '23',
                '_ref': 'string',
                'applicationOwner': 'string',
                'type': 'passenger',
                'cars': [
                    {
                        'id': 'string',
                        '_ref': 'string',
                        'owner': 'string',
                        'properties': [
                            {
                                'name': 'string',
                                'value': 'string'
                            }
                        ]
                    }
                ],
                'username': 'Khaleesi',
                'name': 'Daenerys',
                'surname': 'Targaryen',
                'country': 'Valyria',
                'email': 'madre_dragones@got.com',
                'birthdate': '01/01/1990',
                'images': [
                    'string'
                ],
                'balance': [
                    {
                        'currency': 'string',
                        'value': 0
                    }
                ]
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        response_info_user = None
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = {
            'id': 1,
            'passenger_id': '23',
            'trip': 'Aca estaria toda la info...'
        }
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/client/23/trips/1')
        print(response)
        assert_res = json.loads("""
        {
            "id": 1,
            "passenger_id": "23",
            "trip": "Aca estaria toda la info..."
        }""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_informacion_viaje_chofer_mongo(self):
        """Prueba que al obtener la informacion de un viaje que se encuentra en
        mongo"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_info_user = {
            'client_type': 'passenger'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = {
            'id': 1,
            'passenger_id': '23',
            'trip': 'Aca estaria toda la info...'
        }
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/client/23/trips/1')
        print(response)
        assert_res = json.loads("""
        {
            "id": 1,
            "passenger_id": "23",
            "trip": "Aca estaria toda la info..."
        }""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_informacion_viaje_chofer_mongo2(self):
        """Prueba que al obtener la informacion de un viaje que se encuentra en
        mongo y el usuario no estaba en mongo"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'user': {
                'id': '23',
                '_ref': 'string',
                'applicationOwner': 'string',
                'type': 'driver',
                'cars': [
                    {
                        'id': 'string',
                        '_ref': 'string',
                        'owner': 'string',
                        'properties': [
                            {
                                'name': 'string',
                                'value': 'string'
                            }
                        ]
                    }
                ],
                'username': 'Khaleesi',
                'name': 'Daenerys',
                'surname': 'Targaryen',
                'country': 'Valyria',
                'email': 'madre_dragones@got.com',
                'birthdate': '01/01/1990',
                'images': [
                    'string'
                ],
                'balance': [
                    {
                        'currency': 'string',
                        'value': 0
                    }
                ]
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        response_info_user = None
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = {
            'id': 1,
            'driver_id': '23',
            'trip': 'Aca estaria toda la info...'
        }
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/driver/23/trips/1')
        print(response)
        assert_res = json.loads("""
        {
            "id": 1,
            "driver_id": "23",
            "trip": "Aca estaria toda la info..."
        }""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_informacion_viaje_cliente_sin_autorizacion(self):
        """Prueba que al obtener la informacion de un viaje de un cliente sin autorizacion"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_info_user = {
            'client_type': 'passenger'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = None
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
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
        response_info_user = {
            'client_type': 'passenger'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = None
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
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
        response_info_user = {
            'client_type': 'passenger'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = None
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/client/2/trips/1')
        print(response)
        assert_res = json.loads("""
        {
            "code": -21,
            "message": "El viaje 1 no pertenece al usuario."
        }""")
        self.assertEqual(response.status_code, 401)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_informacion_cliente_viaje_de_otro_cliente_mongo(self):
        """Prueba que al obtener la informacion de un viaje que se encuentra en
        mongo y el usuario no era de este cliente"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'user': {
                'id': '23',
                '_ref': 'string',
                'applicationOwner': 'string',
                'type': 'driver',
                'cars': [
                    {
                        'id': 'string',
                        '_ref': 'string',
                        'owner': 'string',
                        'properties': [
                            {
                                'name': 'string',
                                'value': 'string'
                            }
                        ]
                    }
                ],
                'username': 'Khaleesi',
                'name': 'Daenerys',
                'surname': 'Targaryen',
                'country': 'Valyria',
                'email': 'madre_dragones@got.com',
                'birthdate': '01/01/1990',
                'images': [
                    'string'
                ],
                'balance': [
                    {
                        'currency': 'string',
                        'value': 0
                    }
                ]
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        response_info_user = None
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = {
            'id': 1,
            'driver_id': '55',
            'trip': 'Aca estaria toda la info...'
        }
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/driver/23/trips/1')
        print(response)
        assert_res = json.loads("""
        {
            "code": -21,
            "message": "El viaje 1 no le pertenece al usuario 23."
        }""")
        self.assertEqual(response.status_code, 400)
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
        response_info_user = {
            'client_type': 'driver'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = None
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
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
        response_info_user = {
            'client_type': 'driver'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = None
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
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
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 401)

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
        response_info_user = {
            'client_type': 'driver'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = None
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
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
        response_info_user = {
            'client_type': 'driver'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = None
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/driver/2/trips/1')
        print(response)
        assert_res = json.loads("""
        {
            "code": -21,
            "message": "El viaje 1 no pertenece al usuario."
        }""")
        self.assertEqual(response.status_code, 401)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    #GET informacion de los viajes de un cliente

    def test_informacion_viajes_cliente(self):
        """Prueba que al obtener la informacion de los viajes de un cliente"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'trips': [
                {
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
                },
                {
                    'id': '1',
                    'applicationOwner': 'App',
                    'driver': 'carolina',
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
                        'value': 105
                    }
                }
            ]
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_trips = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/client/23/trips')
        print(response)
        assert_res = json.loads("""
        [
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
            },
            {
                "id": "1",
                "applicationOwner": "App",
                "driver": "carolina",
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
                    "value": 105
                }
            }
        ]""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_informacion_viajes_cliente_sin_autorizacion(self):
        """Prueba que al obtener la informacion de los viajes de un cliente sin autorizacion"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': '0',
            'message': 'Ups...no tiene autorizacion'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(401)
        SharedServer.get_trips = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/client/8/trips')
        print(response)
        assert_res = json.loads("""
        {
            "code": "0",
            "message": "Ups...no tiene autorizacion"
        }""")
        self.assertEqual(response.status_code, 401)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    # GET informacion de los viajes de un chofer

    def test_informacion_viajes_chofer(self):
        """Prueba que al obtener la informacion de los viajes de un chofer"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'trips': [
                {
                    'id': '1',
                    'applicationOwner': 'App',
                    'driver': '2',
                    'passenger': 'carlos',
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
                },
                {
                    'id': '1',
                    'applicationOwner': 'App',
                    'driver': '2',
                    'passenger': 'pamela',
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
                        'currency': 'tarjeta Azul',
                        'value': 90
                    }
                }
            ]
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_trips = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/driver/2/trips')
        print(response)
        assert_res = json.loads("""
        [
            {
                "id": "1",
                "applicationOwner": "App",
                "driver": "2",
                "passenger": "carlos",
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
            },
            {
                "id": "1",
                "applicationOwner": "App",
                "driver": "2",
                "passenger": "pamela",
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
                    "currency": "tarjeta Azul",
                    "value": 90
                }
            }
        ]""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_informacion_viajes_chofer_sin_autorizacion(self):
        """Prueba que al obtener la informacion de los viaje de un chofer sin autorizacion"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': '0',
            'message': 'Ups...no tiene autorizacion'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(401)
        SharedServer.get_trips = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/driver/8/trips')
        print(response)
        assert_res = json.loads("""
        {
            "code": "0",
            "message": "Ups...no tiene autorizacion"
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

    # Aceptar viaje

    def test_aceptar_viaje(self):
        """Probar que un chofer puede aceptar un viaje que no tiene un chofer seleccionado por
            el cliente"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_info_user = {
            'client_type': 'driver'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = {}
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.accept_trip = MagicMock(return_value=True)
        response_mock = True
        ModelManager.accept_trip = MagicMock(return_value=response_mock)
        response = self.app.put('/api/v1/driver/23/trips/12/accept', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 0,
            "message": "El chofer 23 acepto el viaje 12."
        }""")
        self.assertEqual(response.status_code, 201)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_aceptar_viaje_libre_error_mongo(self):
        """Probar que un chofer al aceptar un viaje que no tiene chofer seleccionado, mongo tira un error"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value={
            'client_type': 'driver'
        })
        ModelManager.get_trip = MagicMock(return_value={})
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.accept_trip = MagicMock(return_value=False)
        response = self.app.put('/api/v1/driver/25/trips/13/accept', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -1,
            "message": "El chofer 25 no pudo aceptar el viaje 13, vuelva a intentarlo mas tarde."
        }""")
        self.assertEqual(response.status_code, 400)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_aceptar_viaje_chofer_seleccionado(self):
        """Probar que un chofer, que fue seleccionado por el cliente para este viaje,
           puede aceptarlo"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_info_user = {
            'client_type': 'driver'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = {
            'driver_id': '23'
        }
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.accept_trip = MagicMock(return_value=True)
        response = self.app.put('/api/v1/driver/23/trips/12/accept', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 0,
            "message": "El chofer 23 acepto el viaje 12."
        }""")
        self.assertEqual(response.status_code, 201)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_aceptar_viaje_chofer_seleccionado_error_mongo(self):
        """Probar que un chofer, que fue seleccionado para el viaje por el cliente, al aceptar un viaje,
            mongo tira un error"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_info_user = {
            'client_type': 'driver'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = {
            'driver_id': '25'
        }
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.accept_trip = MagicMock(return_value=False)
        response = self.app.put('/api/v1/driver/25/trips/13/accept', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -1,
            "message": "El chofer 25 no pudo aceptar el viaje 13, vuelva a intentarlo mas tarde."
        }""")
        self.assertEqual(response.status_code, 400)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_error_aceptar_viaje_cliente(self):
        """Probar que un cliente acepte un viaje, debe fallar porque solo los choferes pueden"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_info_user = {
            'client_type': 'passenger'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response = self.app.put('/api/v1/driver/2/trips/13/accept', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -11,
            "message": "El usuario 2 no es un chofer."
        }""")
        self.assertEqual(response.status_code, 400)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
    
    def test_error_aceptar_viaje_inexistente(self):
        """Probar que no se puede aceptar un viaje inexistente"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value={
            'client_type': 'driver'
        })
        ModelManager.get_trip = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.accept_trip = MagicMock(return_value=True)
        ModelManager.accept_trip = MagicMock(return_value=True)
        response = self.app.put('/api/v1/driver/2/trips/0/accept', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -20,
            "message": "El viaje 0 no existe."
        }""")
        self.assertEqual(response.status_code, 404)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_aceptar_viaje_otro_chofer_seleccionado_error(self):
        """Probar que un chofer, que NO fue seleccionado para el viaje por el cliente,
            no pueda aceptar el viaje"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_info_user = {
            'client_type': 'driver'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = {
            'driver_id': '80'
        }
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        response_mock = 1
        ModelManager.accept_trip = MagicMock(return_value=response_mock)
        response = self.app.put('/api/v1/driver/25/trips/13/accept', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -21,
            "message": "El viaje 13 no le pertenece al usuario 25."
        }""")
        self.assertEqual(response.status_code, 400)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_aceptar_viaje_libre_sin_info_chofer_mongo(self):
        """Probar que un chofer puede aceptar un viaje que no tiene un chofer seleccionado por
            el cliente y teniendo en cuenta que no hay informacion en Mongo, sino hay que buscar
            en el shared server"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'user': {
                'id': '23',
                '_ref': 'string',
                'applicationOwner': 'string',
                'type': 'driver',
                'cars': [
                    {
                        'id': 'string',
                        '_ref': 'string',
                        'owner': 'string',
                        'properties': [
                            {
                                'name': 'string',
                                'value': 'string'
                            }
                        ]
                    }
                ],
                'username': 'Khaleesi',
                'name': 'Daenerys',
                'surname': 'Targaryen',
                'country': 'Valyria',
                'email': 'madre_dragones@got.com',
                'birthdate': '01/01/1990',
                'images': [
                    'string'
                ],
                'balance': [
                    {
                        'currency': 'string',
                        'value': 0
                    }
                ]
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        ModelManager.get_trip = MagicMock(return_value={
            'driver_id': '23'
        })
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.accept_trip = MagicMock(return_value=True)
        response = self.app.put('/api/v1/driver/23/trips/12/accept', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 0,
            "message": "El chofer 23 acepto el viaje 12."
        }""")
        self.assertEqual(response.status_code, 201)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_aceptar_viaje_libre_sin_info_chofer_mongo_error(self):
        """Probar que un chofer puede aceptar un viaje que no tiene un chofer seleccionado por
            el cliente y teniendo en cuenta que no hay informacion en Mongo, sino hay que buscar
            en el shared server"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.get_trip = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.accept_trip = MagicMock(return_value=True)
        ModelManager.accept_trip = MagicMock(return_value=True)

        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 9,
            'message': 'No existe el cliente.'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(404)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        response = self.app.put('/api/v1/driver/44/trips/12/accept', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -10,
            "message": "El usuario 44 no existe."
        }""")
        self.assertEqual(response.status_code, 404)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    # Comenzar viaje

    def test_comenzar_viaje(self):
        """Probar que un pasajero puede comenzar un viaje"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_info_user = {
            'client_type': 'passenger'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = {
            'passenger_id' : '23',
            'is_accepted' : True
        }
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.start_trip = MagicMock(return_value=True)
        response = self.app.put('/api/v1/client/23/trips/12/start', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 0,
            "message": "El viaje 12 ha comenzado."
        }""")
        self.assertEqual(response.status_code, 201)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_comenzar_viaje_error_sin_chofer(self):
        """Probar que no se puede comenzar un viaje si el mismo no tiene un chofer que haya aceptado el viaje"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_info_user = {
            'passenger_id' : '23',
            'client_type': 'passenger'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = {
            'passenger_id' : '23',
            'is_accepted': False
        }
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.start_trip = MagicMock(return_value=True)
        response = self.app.put('/api/v1/client/23/trips/12/start', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -22,
            "message": "El viaje 12 no fue aceptado por el chofer."
        }""")
        self.assertEqual(response.status_code, 400)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_error_comenzar_viaje_otro_cliente(self):
        """Probar que un cliente no puede comenzar un viaje si el mismo no le pertenece"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_info_user = {
            'client_type': 'passenger'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = {
            'passenger_id' : '23',
            'is_accepted' : True
        }
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        response = self.app.put('/api/v1/client/2/trips/13/start', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -21,
            "message": "El viaje 13 no le pertenece al usuario 2."
        }""")
        self.assertEqual(response.status_code, 400)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
    
    def test_error_comenzar_viaje_inexistente(self):
        """Probar que no se puede comenzar un viaje inexistente"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value={
            'client_type': 'passenger'
        })
        ModelManager.get_trip = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.start_trip = MagicMock(return_value=True)
        response = self.app.put('/api/v1/client/2/trips/0/start', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -20,
            "message": "El viaje 0 no existe."
        }""")
        self.assertEqual(response.status_code, 404)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_comenzar_viaje_cliente_pedir_info_mongo(self):
        """Probar que un cliente puede comenzar un viaje aun cuando se tiene que pedir la
            informacion del cliente al sharedserver"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'user': {
                'id': '23',
                '_ref': 'string',
                'applicationOwner': 'string',
                'type': 'passenger',
                'cars': [
                    {
                        'id': 'string',
                        '_ref': 'string',
                        'owner': 'string',
                        'properties': [
                            {
                                'name': 'string',
                                'value': 'string'
                            }
                        ]
                    }
                ],
                'username': 'Khaleesi',
                'name': 'Daenerys',
                'surname': 'Targaryen',
                'country': 'Valyria',
                'email': 'madre_dragones@got.com',
                'birthdate': '01/01/1990',
                'images': [
                    'string'
                ],
                'balance': [
                    {
                        'currency': 'string',
                        'value': 0
                    }
                ]
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        ModelManager.get_trip = MagicMock(return_value= {
            'passenger_id' : '23',
            'is_accepted' : True
        })
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.start_trip = MagicMock(return_value=True)
        response = self.app.put('/api/v1/client/23/trips/12/start', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 0,
            "message": "El viaje 12 ha comenzado."
        }""")
        self.assertEqual(response.status_code, 201)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_comenzar_viaje_libre_sin_info_cliente_mongo_error(self):
        """Probar que un cliente no puede comenzar un viaje si no se tiene la informacion del cliente,
            en este caso vamos a hacer que el sharedserver tire error al pedir la informacion del mismo"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.get_trip = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.start_trip = MagicMock(return_value=True)

        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 9,
            'message': 'No existe el cliente.'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(404)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        response = self.app.put('/api/v1/client/44/trips/12/start', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -10,
            "message": "El usuario 44 no existe."
        }""")
        self.assertEqual(response.status_code, 404)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    # Finalizar viaje

    def test_finalizar_viaje(self):
        """Probar que un pasajero puede finalizar un viaje"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_info_user = {
            'client_type': 'passenger'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = {
            'passenger_id' : '23',
            'start_stamp' : '01/05/2017 1:05'
        }
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.end_trip = MagicMock(return_value=True)
        ModelManager.delete_trip = MagicMock(return_value=True)
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 0,
            'message': 'Se guardo correctamente el viaje.'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(201)
        SharedServer.post_trip =  MagicMock(return_value=response_mock)
        response = self.app.put('/api/v1/client/23/trips/12/finish', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 0,
            "message": "El viaje 12 ha finalizado."
        }""")
        self.assertEqual(response.status_code, 201)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_finalizar_viaje_error_no_comenzo(self):
        """Probar que no se puede finalizar un viaje si el mismo no comenzo"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_info_user = {
            'passenger_id' : '23',
            'client_type': 'passenger'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = {
            'passenger_id' : '23'
        }
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.end_trip = MagicMock(return_value=True)
        response = self.app.put('/api/v1/client/23/trips/12/finish', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -8,
            "message": "El viaje 12 no fue comenzado."
        }""")
        self.assertEqual(response.status_code, 400)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_error_finalizar_viaje_otro_cliente(self):
        """Probar que un cliente no puede finalizar un viaje si el mismo no le pertenece"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_info_user = {
            'client_type': 'passenger'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = {
            'passenger_id' : '23',
            'start_stamp' : '01/05/2017 1:05'
        }
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        response = self.app.put('/api/v1/client/2/trips/13/finish', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -21,
            "message": "El viaje 13 no le pertenece al usuario 2."
        }""")
        self.assertEqual(response.status_code, 400)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
    
    def test_error_finalizar_viaje_inexistente(self):
        """Probar que no se puede finalizar un viaje inexistente"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value={
            'client_type': 'passenger'
        })
        ModelManager.get_trip = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.end_trip = MagicMock(return_value=True)
        response = self.app.put('/api/v1/client/2/trips/0/finish', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -20,
            "message": "El viaje 0 no existe."
        }""")
        self.assertEqual(response.status_code, 404)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_finalizar_viaje_cliente_pedir_info_mongo(self):
        """Probar que un cliente puede finalizar un viaje aun cuando se tiene que pedir la
            informacion del cliente al sharedserver"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'user': {
                'id': '23',
                '_ref': 'string',
                'applicationOwner': 'string',
                'type': 'passenger',
                'cars': [
                    {
                        'id': 'string',
                        '_ref': 'string',
                        'owner': 'string',
                        'properties': [
                            {
                                'name': 'string',
                                'value': 'string'
                            }
                        ]
                    }
                ],
                'username': 'Khaleesi',
                'name': 'Daenerys',
                'surname': 'Targaryen',
                'country': 'Valyria',
                'email': 'madre_dragones@got.com',
                'birthdate': '01/01/1990',
                'images': [
                    'string'
                ],
                'balance': [
                    {
                        'currency': 'string',
                        'value': 0
                    }
                ]
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        ModelManager.get_trip = MagicMock(return_value={
            'passenger_id' : '23',
            'start_stamp' : '01/05/2017 1:05'
        })
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.finish_trip = MagicMock(return_value=True)
        response_info_user = None
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response = self.app.put('/api/v1/client/23/trips/12/finish', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 0,
            "message": "El viaje 12 ha finalizado."
        }""")
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 201)

    def test_finalizar_viaje_libre_sin_info_cliente_mongo_error(self):
        """Probar que un cliente no puede finalizar un viaje si no se tiene la informacion del cliente,
            en este caso vamos a hacer que el sharedserver tire error al pedir la informacion del mismo"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.get_trip = MagicMock(return_value={})
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.start_trip = MagicMock(return_value=True)
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 9,
            'message': 'No existe el cliente.'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(404)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        response = self.app.put('/api/v1/client/44/trips/12/finish', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -10,
            "message": "El usuario 44 no existe."
        }""")
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 404)

    #Post ultima ubicacion de un usuario

    def test_ultima_ubicacion_valida_chofer(self):
        """Probar que un chofer puede enviar una ubicacion valida para guardarla"""
        data = {
            "user_id": "llevame-oscar",
            "lat": "-34.627277",
            "long": "-58.681433",
            "accuracy": "1"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value={
            "type": "driver"
        })
        ModelManager.add_last_known_position = MagicMock(return_value=True)
        response = self.app.post('/api/v1/lastlocation', data=json.dumps(data),
                                      content_type='application/json', follow_redirects=True)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 0,
            "message": "Se actualizo la ubicacion del usuario llevame-oscar."
        }""")
        print(response.data)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 201)

    def test_ultima_ubicacion_valida_cliente_sin_viajes(self):
        """Probar que un cliente puede enviar una ubicacion valida para guardarla aun cuando 
           no comenzo un viaje"""
        data = {
            "user_id": "llevame-oscar",
            "lat": "-34.627277",
            "long": "-58.681433",
            "accuracy": "1"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value={
            "type": "passenger"
        })
        ModelManager.add_last_known_position = MagicMock(return_value=True)
        ModelManager.trips_by_client = MagicMock(return_value=None)
        response = self.app.post('/api/v1/lastlocation', data=json.dumps(data),
                                      content_type='application/json', follow_redirects=True)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 0,
            "message": "Se actualizo la ubicacion del usuario llevame-oscar."
        }""")
        print(response.data)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 201)

    def test_ultima_ubicacion_valida_cliente_con_viajes_finalizados(self):
        """Probar que un cliente puede enviar una ubicacion valida y tiene
           viajes finalizados"""
        data = {
            "user_id": "llevame-oscar",
            "lat": "-34.627277",
            "long": "-58.681433",
            "accuracy": "1"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value={
            "type": "passenger"
        })
        ModelManager.add_last_known_position = MagicMock(return_value=True)
        trips = [
            {
                'id': '1',
                'start_stamp': 'comenzo...',
                'end_stamp': 'finalizo...'
            },
            {
                'id': '2',
                'start_stamp': 'comenzo...',
                'end_stamp': 'finalizo...'
            }
        ]
        ModelManager.trips_by_client = MagicMock(return_value=trips)
        ModelManager.add_location_to_trip = MagicMock(return_value=False)
        response = self.app.post('/api/v1/lastlocation', data=json.dumps(data),
                                      content_type='application/json', follow_redirects=True)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 0,
            "message": "Se actualizo la ubicacion del usuario llevame-oscar."
        }""")
        print(response.data)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 201)

    def test_ultima_ubicacion_valida_cliente_con_viaje_sin_finalizar(self):
        """Probar que un cliente puede enviar una ubicacion valida y tiene
           viajes sin finalizar"""
        data = {
            "user_id": "llevame-oscar",
            "lat": "-34.627277",
            "long": "-58.681433",
            "accuracy": "1"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value={
            "type": "passenger"
        })
        ModelManager.add_last_known_position = MagicMock(return_value=True)
        trips = [
            {
                'id': '1',
                'start_stamp': 'comenzo...',
                'end_stamp': 'finalizo...'
            },
            {
                'id': '2',
                'start_stamp': 'comenzo...'
            }
        ]
        ModelManager.trips_by_client = MagicMock(return_value=trips)
        ModelManager.add_location_to_trip = MagicMock(return_value=True)
        ModelManager.add_location_to_trip = MagicMock(return_value=False)
        response = self.app.post('/api/v1/lastlocation', data=json.dumps(data),
                                      content_type='application/json', follow_redirects=True)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 0,
            "message": "Se actualizo la ubicacion del usuario llevame-oscar."
        }""")
        print(response.data)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 201)

    def test_ultima_ubicacion_valida_error_mongo(self):
        """Probar que un cliente puede enviar una ubicacion valida para guardarla 
           pero fallo al guardar la ubicacion"""
        data = {
            "user_id": "llevame-oscar",
            "lat": "-34.627277",
            "long": "-58.681433",
            "accuracy": "1"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value={})
        ModelManager.add_last_known_position = MagicMock(return_value=False)
        response = self.app.post('/api/v1/lastlocation', data=json.dumps(data),
                                      content_type='application/json', follow_redirects=True)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -1,
            "message": "No se pudo guardar la ubicacion del usuario llevame-oscar, intentelo mas tarde."
        }""")
        print(response.data)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 400)

    def test_ultima_ubicacion_valida_buscar_usuario_sin_viajes(self):
        """Probar que un cliente puede enviar una ubicacion valida para guardarla y como
           el usuario no se encuentra en la base de datos se tuvo que buscar en shared server"""
        data = {
            "user_id": "llevame-oscar",
            "lat": "-34.627277",
            "long": "-58.681433",
            "accuracy": "1"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_last_known_position = MagicMock(return_value=True)
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'user': {
                'id': '23',
                '_ref': 'string',
                'applicationOwner': 'string',
                'type': 'passenger',
                'cars': [
                    {
                        'id': 'string',
                        '_ref': 'string',
                        'owner': 'string',
                        'properties': [
                            {
                                'name': 'string',
                                'value': 'string'
                            }
                        ]
                    }
                ],
                'username': 'Khaleesi',
                'name': 'Daenerys',
                'surname': 'Targaryen',
                'country': 'Valyria',
                'email': 'madre_dragones@got.com',
                'birthdate': '01/01/1990',
                'images': [
                    'string'
                ],
                'balance': [
                    {
                        'currency': 'string',
                        'value': 0
                    }
                ]
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        ModelManager.trips_by_client = MagicMock(return_value=None)
        response = self.app.post('/api/v1/lastlocation', data=json.dumps(data),
                                      content_type='application/json', follow_redirects=True)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 0,
            "message": "Se actualizo la ubicacion del usuario llevame-oscar."
        }""")
        print(response.data)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 201)

    def test_ultima_ubicacion_valida_buscar_usuario_error_mongo(self):
        """Probar que un cliente puede enviar una ubicacion valida para guardarla y como
           el usuario no se encuentra en la base de datos se tuvo que buscar en shared server
           pero falla al guardar la informacion de la ubicacion en mongo"""
        data = {
            "user_id": "llevame-oscar",
            "lat": "-34.627277",
            "long": "-58.681433",
            "accuracy": "1"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_last_known_position = MagicMock(return_value=False)
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'user': {
                'id': '23',
                '_ref': 'string',
                'applicationOwner': 'string',
                'type': 'passenger',
                'cars': [
                    {
                        'id': 'string',
                        '_ref': 'string',
                        'owner': 'string',
                        'properties': [
                            {
                                'name': 'string',
                                'value': 'string'
                            }
                        ]
                    }
                ],
                'username': 'Khaleesi',
                'name': 'Daenerys',
                'surname': 'Targaryen',
                'country': 'Valyria',
                'email': 'madre_dragones@got.com',
                'birthdate': '01/01/1990',
                'images': [
                    'string'
                ],
                'balance': [
                    {
                        'currency': 'string',
                        'value': 0
                    }
                ]
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        response = self.app.post('/api/v1/lastlocation', data=json.dumps(data),
                                      content_type='application/json', follow_redirects=True)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -1,
            "message": "No se pudo guardar la ubicacion del usuario llevame-oscar, intentelo mas tarde."
        }""")
        print(response.data)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 400)

    def test_ultima_ubicacion_valida_usuario_inexistente(self):
        """Probar que un cliente puede enviar una ubicacion valida para guardarla pero
           el mismo no existe ni en mongo ni el shared"""
        data = {
            "user_id": "llevame-oscar",
            "lat": "-34.627277",
            "long": "-58.681433",
            "accuracy": "1"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_last_known_position = MagicMock(return_value=False)
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 8,
            'menssage': 'Ups... no existe el usuario'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(401)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        response = self.app.post('/api/v1/lastlocation', data=json.dumps(data),
                                 content_type='application/json', follow_redirects=True)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -10,
            "message": "El usuario llevame-oscar no existe."
        }""")
        print(response.data)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 404)

    #Get ultima ubicacion de un usuario

    def test_get_ultima_ubicacion_valida(self):
        """Probar que un cliente puede obtener una ubicacion valida para guardarla"""
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value={})
        ModelManager.get_last_known_position = MagicMock(return_value={
            'lat': '-54.627277',
            'long': '-58.681433',
            'accuracy': '1',
            'timestamp': '01/05/2017 1:05'
        })
        response = self.app.get('/api/v1/lastlocation/23')
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "lat": "-54.627277",
            "long": "-58.681433",
            "accuracy": "1",
            "timestamp": "01/05/2017 1:05"
        }""")
        print(response.data)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 200)

    def test_get_ultima_ubicacion_valida_error_mongo(self):
        """Probar que un cliente no puede obtener una ubicacion que no existe.
           El usuario existe """
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value={})
        ModelManager.get_last_known_position = MagicMock(return_value=None)
        response = self.app.get('/api/v1/lastlocation/23')
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -1,
            "message": "La ubicacion del usuario con id 23 no existe."
        }""")
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 400)

    def test_get_ultima_ubicacion_no_existente_buscar_usuario(self):
        """Probar que un cliente no puede obtener una ubicacion valida porque no existe
           la ubicacion y el usuario existe en el shared pero no en mongo"""
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.get_last_known_position = MagicMock(return_value=None)
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'user': {
                'id': '23',
                '_ref': 'string',
                'applicationOwner': 'string',
                'type': 'passenger',
                'cars': [
                    {
                        'id': 'string',
                        '_ref': 'string',
                        'owner': 'string',
                        'properties': [
                            {
                                'name': 'string',
                                'value': 'string'
                            }
                        ]
                    }
                ],
                'username': 'Khaleesi',
                'name': 'Daenerys',
                'surname': 'Targaryen',
                'country': 'Valyria',
                'email': 'madre_dragones@got.com',
                'birthdate': '01/01/1990',
                'images': [
                    'string'
                ],
                'balance': [
                    {
                        'currency': 'string',
                        'value': 0
                    }
                ]
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        response = self.app.get('/api/v1/lastlocation/23')
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -1,
            "message": "La ubicacion del usuario con id 23 no existe."
        }""")
        print(response.data)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 400)

    def test_get_ultima_ubicacion_valida_usuario_inexistente(self):
        """Probar que un cliente puede enviar una ubicacion valida para guardarla pero
           el mismo no existe ni en mongo ni el shared"""
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_last_known_position = MagicMock(return_value=False)
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 8,
            'menssage': 'Ups... no existe el usuario'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(401)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        response = self.app.get('/api/v1/lastlocation/23')
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -10,
            "message": "El usuario 23 no existe."
        }""")
        print(response.data)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 404)

    # Rechazar viaje

    def test_error_rechazar_viaje_sin_chofer(self):
        """Probar que un chofer no puede rechazar un viaje que no tiene un chofer seleccionado por
            el cliente"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_info_user = {
            'client_type': 'driver'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = {}
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.accept_trip = MagicMock(return_value=True)
        response_mock = False
        ModelManager.refuse_trip = MagicMock(return_value=response_mock)
        response = self.app.put('/api/v1/driver/23/trips/12/refuse', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -21,
            "message": "El viaje 12 no le pertenece al chofer 23."
        }""")
        self.assertEqual(response.status_code, 400)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
    
    def test_rechazar_viaje_chofer_seleccionado(self):
        """Probar que un chofer, que fue seleccionado por el cliente para este viaje,
           puede rechazarlo"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_info_user = {
            'client_type': 'driver'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = {
            'driver_id': '23'
        }
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.refuse_trip = MagicMock(return_value=True)
        response = self.app.put('/api/v1/driver/23/trips/12/refuse', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 0,
            "message": "El chofer 23 rechazo el viaje 12."
        }""")
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 201)

    def test_rechazar_viaje_chofer_seleccionado_error_mongo(self):
        """Probar que un chofer, que fue seleccionado para el viaje por el cliente, al rechazar un viaje,
            mongo tira un error"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_info_user = {
            'client_type': 'driver'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = {
            'driver_id': '25'
        }
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.refuse_trip = MagicMock(return_value=False)
        response = self.app.put('/api/v1/driver/25/trips/13/refuse', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -1,
            "message": "El chofer 25 no pudo rechazar el viaje 13, vuelva a intentarlo mas tarde."
        }""")
        self.assertEqual(response.status_code, 400)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_error_rechazar_viaje_cliente(self):
        """Probar que un cliente rechaza un viaje, debe fallar porque solo los choferes pueden"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_info_user = {
            'client_type': 'passenger'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response = self.app.put('/api/v1/driver/2/trips/13/refuse', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -11,
            "message": "El usuario 2 no es un chofer."
        }""")
        self.assertEqual(response.status_code, 400)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
    
    def test_error_rechazar_viaje_inexistente(self):
        """Probar que no se puede rechazar un viaje inexistente"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value={
            'client_type': 'driver'
        })
        ModelManager.get_trip = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.refuse_trip = MagicMock(return_value=True)
        response = self.app.put('/api/v1/driver/2/trips/0/refuse', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -20,
            "message": "El viaje 0 no existe."
        }""")
        self.assertEqual(response.status_code, 404)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_rechazar_viaje_otro_chofer_seleccionado_error(self):
        """Probar que un chofer, que NO fue seleccionado para el viaje por el cliente,
            no pueda rechazar el viaje"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        response_info_user = {
            'client_type': 'driver'
        }
        ModelManager.get_info_usuario = MagicMock(return_value=response_info_user)
        response_info_trip = {
            'driver_id': '80'
        }
        ModelManager.get_trip = MagicMock(return_value=response_info_trip)
        # response_mock = True
        # ModelManager.refuse_trip = MagicMock(return_value=response_mock)
        response = self.app.put('/api/v1/driver/25/trips/13/refuse', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -21,
            "message": "El viaje 13 no le pertenece al usuario 25."
        }""")
        self.assertEqual(response.status_code, 400)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_rechazar_viaje_sin_info_chofer_mongo(self):
        """Probar que un chofer puede rechazar un viaje, teniendo en cuenta que no hay informacion 
            en Mongo y se tuvo que buscar en el shared server"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'user': {
                'id': '23',
                '_ref': 'string',
                'applicationOwner': 'string',
                'type': 'driver',
                'cars': [
                    {
                        'id': 'string',
                        '_ref': 'string',
                        'owner': 'string',
                        'properties': [
                            {
                                'name': 'string',
                                'value': 'string'
                            }
                        ]
                    }
                ],
                'username': 'Khaleesi',
                'name': 'Daenerys',
                'surname': 'Targaryen',
                'country': 'Valyria',
                'email': 'madre_dragones@got.com',
                'birthdate': '01/01/1990',
                'images': [
                    'string'
                ],
                'balance': [
                    {
                        'currency': 'string',
                        'value': 0
                    }
                ]
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        ModelManager.get_trip = MagicMock(return_value={
            'driver_id': '23'
        })
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.refuse_trip = MagicMock(return_value=True)
        response = self.app.put('/api/v1/driver/23/trips/12/refuse', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 0,
            "message": "El chofer 23 rechazo el viaje 12."
        }""")
        self.assertEqual(response.status_code, 201)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_rechazar_viaje_sin_info_chofer_mongo_error(self):
        """Probar que un chofer puede rechazar un viaje, teniendo en cuenta que no hay informacion 
            en Mongo, sino hay que buscar en el shared server"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.get_trip = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.refuse_trip = MagicMock(return_value=True)

        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 9,
            'message': 'No existe el cliente.'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(404)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        response = self.app.put('/api/v1/driver/44/trips/12/refuse', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -10,
            "message": "El usuario 44 no existe."
        }""")
        self.assertEqual(response.status_code, 404)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    # Modificar chofer de un viaje

    def test_modificar_chofer_viaje_sin_info_chofer_mongo_error(self):
        """Probar que un chofer no puede modificar el chofer de un viaje, teniendo en cuenta que no hay
            informacion del cliente"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.get_trip = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)

        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 9,
            'message': 'No existe el cliente.'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(404)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        response = self.app.put('/api/v1/client/44/trips/12/driver/1', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -10,
            "message": "El usuario 44 no existe."
        }""")
        self.assertEqual(response.status_code, 404)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_modificar_chofer_viaje_sin_info_cliente_mongo(self):
        """Probar que un cliente no puede modificar un viaje si el mismo no existe, teniendo en
           cuenta que no hay informacion en Mongo, se tuvo que buscar en el shared server y el usuario
           es un conductor"""
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'user': {
                'id': '23',
                '_ref': 'string',
                'applicationOwner': 'string',
                'type': 'driver',
                'cars': [
                    {
                        'id': 'string',
                        '_ref': 'string',
                        'owner': 'string',
                        'properties': [
                            {
                                'name': 'string',
                                'value': 'string'
                            }
                        ]
                    }
                ],
                'username': 'Khaleesi',
                'name': 'Daenerys',
                'surname': 'Targaryen',
                'country': 'Valyria',
                'email': 'madre_dragones@got.com',
                'birthdate': '01/01/1990',
                'images': [
                    'string'
                ],
                'balance': [
                    {
                        'currency': 'string',
                        'value': 0
                    }
                ]
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        ModelManager.get_trip = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.add_driver_to_trip = MagicMock(return_value=True)
        ModelManager.refuse_trip = MagicMock(return_value=True)
        response = self.app.put('/api/v1/client/23/trips/12/driver/1', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": -12,
            "message": "El usuario 23 no es un pasajero."
        }""")
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 400)
