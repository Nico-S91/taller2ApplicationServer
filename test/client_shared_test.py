""" @package test.client_shared_test
"""
import unittest
import mock
from service.login_service import LoginService
import json
import main_app
import requests
from model import db_manager
from mock import MagicMock
from service.shared_server import SharedServer
from api.client_controller import ClientController
from api.model_manager import ModelManager
from flask import jsonify
from test.response_mock import ResponseMock

class TestClientController(unittest.TestCase):
    """Esta clase tiene los test de los endpoint del controller_client
    """
    def setUp(self):
        # creates a test client
        self.app = main_app.application.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True
        SharedServer._get_token_initial = mock.MagicMock(return_value='')
        SharedServer._refresh_token = mock.MagicMock(return_value='')

    def mockeamos_login_correcto(self):
        """Mockeamos para que el login de correcto"""
        LoginService.is_logged = mock.MagicMock(return_value=SharedServer)

    def test_home_status_code(self):
        """Prueba el endpoint HelloWordl"""
        self.mockeamos_login_correcto()
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        print(str(result.data))
        self.assertEqual(result.data, b'{\n  "message": "hello world"\n}\n')

    #Pruebas del login
    # def test_login_correcto(self):
    #     """Pruebo que se loguee correctamente el usuario"""
    #     response_api = json.loads("""
    #     {
    #         "respuesta": "Se logueo correctamente",
    #     }
    #     """)
    #     LoginService.login = mock.MagicMock(return_value=response_api)
    #     response = self.app.post('/login/username/user/password/pass')
    #     print(str(response.data))
    #     self.assertTrue(LoginService.login.called)
    #     self.assertEqual(response.status_code, 200)
    #     cmp_response = json.loads(response.data)
    #     self.assertEqual(response_api, cmp_response)

    # def test_login_con_usuario_o_contrasenia_incorrecta(self):
    #     """Pruebo que se loguee correctamente el usuario"""
    #     LoginService.login = mock.MagicMock(return_value=False)
    #     response = self.app.post('/login/username/ /password/ ')
    #     print('*********************************************')
    #     print(str(response.data))
    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(response.data, b'{\n  "respuesta": "Credenciales invalidas"\n}\n')

    # def test_login_facebook_correcto(self):
    #     """Pruebo que se loguee correctamente el usuario"""
    #     LoginService.login_facebook = mock.MagicMock(return_value=True)
    #     response = self.app.post('/login/facebookAuthToken/user')
    #     print(str(response.data))
    #     self.assertTrue(LoginService.login.called)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data, b'{\n  "respuesta": "Se logueo correctamente"\n}\n')

    # def test_login_facebook_incorrecta(self):
    #     """Pruebo que se loguee correctamente el usuario"""
    #     LoginService.login_facebook = mock.MagicMock(return_value=False)
    #     response = self.app.post('/login/facebookAuthToken/245')
    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(response.data, b'{\n  "respuesta": "Credenciales invalidas"\n}\n')

    def test_logout_correcto(self):
        """Pruebo que se desloguee correctamente el usuario"""
        LoginService.logout = mock.MagicMock(return_value=True)
        response = self.app.post('/logout')
        print(str(response.data))
        self.assertTrue(LoginService.logout.called)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{\n  "mensaje": "Se deslogueo correctamente"\n}\n')

    #Pruebas de chofer

    #Get chofer

    def test_obtener_chofer(self):
        """Prueba que al obtener un chofer este sea igual al que viene por defecto"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'user': {
                'id': '23',
                '_ref': 'string',
                'applicationOwner': 'string',
                'type': 'chofer',
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
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/driver/23')
        assert_res = json.loads("""
        {
            "id": "23",
            "_ref": "string",
            "applicationOwner": "string",
            "type": "chofer",
            "cars": [
            {
                "id": "string",
                "_ref": "string",
                "owner": "string",
                "properties": [
                {
                    "name": "string",
                    "value": "string"
                }
                ]
            }
            ],
            "username": "Khaleesi",
            "name": "Daenerys",
            "surname": "Targaryen",
            "country": "Valyria",
            "email": "madre_dragones@got.com",
            "birthdate": "01/01/1990",
            "images": [
            "string"
            ],
            "balance": [
            {
                "currency": "string",
                "value": 0
            }
            ]
        }""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_chofer_no_autorizado(self):
        """Prueba que al obtener un chofer cuando no esta autorizado"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 1,
            'message': 'No esta autorizado a obtener la info del usuario'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(401)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/driver/23')
        assert_res = json.loads("""{
            "code": 1,
            "message": "No esta autorizado a obtener la info del usuario"
        }""")
        self.assertEqual(response.status_code, 401)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_chofer_no_existe(self):
        """Prueba que al obtener un chofer cuando no existe"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 2,
            'message': 'No existe el usuario'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(404)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/driver/23')
        assert_res = json.loads("""{
            "code": 2,
            "message": "No existe el usuario"
        }""")
        self.assertEqual(response.status_code, 404)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    #Get choferes
    def test_obtener_choferes(self):
        """Prueba que al obtener todos los choferes, viene el default"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'count': 2,
                'total': 2,
                'next': 'string',
                'prev': 'string',
                'first': 'string',
                'last': 'string',
                'version': 'string'
            },
            'users': [
                {
                    'id': 'c1',
                    '_ref': '2werwerfw',
                    'applicationOwner': 'string',
                    'type': 'driver',
                    'cars': [
                        {
                            'id': '1',
                            '_ref': 'erge',
                            'owner': 'c1',
                            'properties': [
                                {
                                    'name': 'color',
                                    'value': 'negro'
                                },
                                {
                                    'name': 'marca',
                                    'value': 'fiat'
                                }
                            ]
                        }
                    ],
                    'username': 'mz',
                    'name': 'martin',
                    'surname': 'tincho',
                    'country': 'argentina',
                    'email': 'm.t@gmail.com',
                    'birthdate': '12/12/2000',
                    'images': [
                        'http://sdfpsdf.com/sfisdjfoosi.jpg'
                    ],
                    'balance': [
                        {
                            'currency': 'peso',
                            'value': 200
                        },
                        {
                            'id': 'c2',
                            '_ref': '2werwedrfw',
                            'applicationOwner': 'string',
                            'type': 'driver',
                            'cars': [
                                {
                                    'id': '1',
                                    '_ref': 'erge',
                                    'owner': 'c1',
                                    'properties': [
                                        {
                                            'name': 'color',
                                            'value': 'rojo'
                                        },
                                        {
                                            'name': 'marca',
                                            'value': 'fiat'
                                        }
                                    ]
                                }
                            ],
                            'username': 'ht',
                            'name': 'homero',
                            'surname': 'simpson',
                            'country': 'argentina',
                            'email': 'h.t@gmail.com',
                            'birthdate': '12/05/1970',
                            'images': [
                                'http://sdfpsdf.com/aaaaaaosi.jpg'
                            ],
                            'balance': [
                                {
                                    'currency': 'peso',
                                    'value': 9000
                                }
                            ]
                        }
                    ]
                }
            ]
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_clients = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/drivers')
        assert_res = json.loads("""[
            {
                "id": "c1",
                "_ref": "2werwerfw",
                "applicationOwner": "string",
                "type": "driver",
                "cars": [
                    {
                        "id": "1",
                        "_ref": "erge",
                        "owner": "c1",
                        "properties": [
                            {
                                "name": "color",
                                "value": "negro"
                            },
                            {
                                "name": "marca",
                                "value": "fiat"
                            }
                        ]
                    }
                ],
                "username": "mz",
                "name": "martin",
                "surname": "tincho",
                "country": "argentina",
                "email": "m.t@gmail.com",
                "birthdate": "12/12/2000",
                "images": [
                    "http://sdfpsdf.com/sfisdjfoosi.jpg"
                ],
                "balance": [
                    {
                        "currency": "peso",
                        "value": 200
                    },
                    {
                        "id": "c2",
                        "_ref": "2werwedrfw",
                        "applicationOwner": "string",
                        "type": "driver",
                        "cars": [
                            {
                                "id": "1",
                                "_ref": "erge",
                                "owner": "c1",
                                "properties": [
                                    {
                                        "name": "color",
                                        "value": "rojo"
                                    },
                                    {
                                        "name": "marca",
                                        "value": "fiat"
                                    }
                                ]
                            }
                        ],
                        "username": "ht",
                        "name": "homero",
                        "surname": "simpson",
                        "country": "argentina",
                        "email": "h.t@gmail.com",
                        "birthdate": "12/05/1970",
                        "images": [
                            "http://sdfpsdf.com/aaaaaaosi.jpg"
                        ],
                        "balance": [
                            {
                                "currency": "peso",
                                "value": 9000
                            }
                        ]
                    }
                ]
            }
        ]""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_choferes_desautorizado(self):
        """Prueba que al obtener todos los choferes sin autorizacion"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 3,
            'message': 'No estas autorizado'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(401)
        SharedServer.get_clients = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/drivers')
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 3,
            "message": "No estas autorizado"
        }""")
        self.assertEqual(response.status_code, 401)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_crear_chofer(self):
        """Prueba que al crear un chofer con la informacion valida entonces devuelva
           un mensaje que se creo correctamente"""
        self.mockeamos_login_correcto()
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'xx'
            },
            'user': {
                'id': 'c1',
                '_ref': '2werwerfw',
                'applicationOwner': 'string',
                'type': 'driver',
                'cars': [
                    {
                        'id': '1',
                        '_ref': 'erge',
                        'owner': 'c1',
                        'properties': [
                            {
                                'name': 'color',
                                'value': 'negro'
                            },
                            {
                                'name': 'marca',
                                'value': 'fiat'
                            }
                        ]
                    }
                ],
                'username': 'mz',
                'name': 'martin',
                'surname': 'tincho',
                'country': 'argentina',
                'email': 'm.t@gmail.com',
                'birthdate': '12/12/2000',
                'images': [
                    'http://sdfpsdf.com/sfisdjfoosi.jpg'
                ],
                'balance': [{
                    'currency': 'peso',
                    'value': 200
                }]
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(201)
        SharedServer.post_client = MagicMock(return_value=response_mock)
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        response = self.app.post('/api/v1/driver', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "id": "c1",
            "_ref": "2werwerfw",
            "applicationOwner": "string",
            "type": "driver",
            "cars": [{
                "id": "1",
                "_ref": "erge",
                "owner": "c1",
                "properties": [{
                    "name": "color",
                    "value": "negro"
                },
                {
                "name": "marca",
                "value": "fiat"
                }]
            }],
            "username": "mz",
            "name": "martin",
            "surname": "tincho",
            "country": "argentina",
            "email": "m.t@gmail.com",
            "birthdate": "12/12/2000",
            "images": [
                "http://sdfpsdf.com/sfisdjfoosi.jpg"
            ],
            "balance": [{
                "currency": "peso",
                "value": 200
            }]
        }""")
        self.assertEqual(response.status_code, 201)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_crear_chofer_insuficientes_parametros(self):
        """Prueba que al crear un chofer con falta de informacion devuelva codigo de error
            de precondiciones"""
        self.mockeamos_login_correcto()
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        #Mockeamos la llamada
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 1,
            'message': 'No se cumplio con las precondiciones'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(400)
        SharedServer.post_client = MagicMock(return_value=response_mock)
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        response = self.app.post('/api/v1/driver', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 1,
            "message": "No se cumplio con las precondiciones"
        }""")
        self.assertEqual(response.status_code, 400)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_crear_chofer_sin_informacion(self):
        """Prueba que al crear un chofer sin mandar la informacion devuelva el codigo de
           error correspondiente"""
        self.mockeamos_login_correcto()
        payload = ''
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.post('/api/v1/driver', data=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

    #Put chofer

    def test_modificar_chofer(self):
        """Prueba que al modificar un chofer con la informacion valida entonces devuelve
           un mensaje que se creo correctamente"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ClientController._get_ref_client = mock.MagicMock(return_value='ref')
        ModelManager.get_info_usuario = MagicMock(return_value={})
        ModelManager.update_usuario = mock.MagicMock(return_value=True)
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': '1'
            },
            'user': {
                'id': 'c1',
                '_ref': '2werwerfw',
                'applicationOwner': 'string',
                'type': 'driver',
                'cars': [
                    {
                        'id': '1',
                        '_ref': 'erge',
                        'owner': 'c1',
                        'properties': [
                            {
                                'name': 'color',
                                'value': 'negro'
                            },
                            {
                                'name': 'marca',
                                'value': 'fiat'
                            }
                        ]
                    }
                ],
                'username': 'mz',
                'name': 'martin',
                'surname': 'tincho',
                'country': 'argentina',
                'email': 'm.t@gmail.com',
                'birthdate': '12/12/2000',
                'images': [
                    'http://sdfpsdf.com/sfisdjfoosi.jpg'
                ],
                'balance': [
                    {
                        'currency': 'peso',
                        'value': 200
                    }
                ]
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(201)
        SharedServer.put_client = MagicMock(return_value=response_mock)
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        ModelManager.get_info_usuario = MagicMock(return_value={})
        ModelManager.update_usuario = MagicMock(return_value=True)
        response = self.app.put(
            '/api/v1/driver/88', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "id": "c1",
            "_ref": "2werwerfw",
            "applicationOwner": "string",
            "type": "driver",
            "cars": [
            {
                "id": "1",
                "_ref": "erge",
                "owner": "c1",
                "properties": [
                {
                    "name": "color",
                    "value": "negro"
                },
            {
                    "name": "marca",
                    "value": "fiat"
                }
                ]
            }
            ],
            "username": "mz",
            "name": "martin",
            "surname": "tincho",
            "country": "argentina",
            "email": "m.t@gmail.com",
            "birthdate": "12/12/2000",
            "images": [
            "http://sdfpsdf.com/sfisdjfoosi.jpg"
            ],
            "balance": [
            {
                "currency": "peso",
                "value": 200
            }]
        }""")
        self.assertEqual(response.status_code, 201)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_modificar_chofer_sin_informacion(self):
        """Prueba que al modificar un chofer sin mandar la informacion devuelva el codigo de
           error correspondiente"""
        self.mockeamos_login_correcto()
        ClientController._get_ref_client = mock.MagicMock(return_value='ref')
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 1,
            'message': 'No se cumplio con las precondiciones'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(400)
        SharedServer.put_client = MagicMock(return_value=response_mock)
        payload = '{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}'
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put(
            '/api/v1/driver/14', data=payload, headers=headers)
        assert_res = json.loads("""{
            "code": 1,
            "message": "No se cumplio con las precondiciones"
        }""")
        print(response.data)

        self.assertEqual(response.status_code, 400)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_modificar_chofer_no_existe(self):
        """Prueba que al modificar un chofer que no existe"""
        self.mockeamos_login_correcto()
        ClientController._get_ref_client = mock.MagicMock(return_value='ref')
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 2,
            'message': 'No existe el usuario'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(404)
        SharedServer.put_client = MagicMock(return_value=response_mock)
        payload = '{\r\n  \"\": \"\"}'
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put(
            '/api/v1/driver/14', data=payload, headers=headers)
        assert_res = json.loads("""{
            "code": 2,
            "message": "No existe el usuario"
        }""")
        self.assertEqual(response.status_code, 404)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_modificar_chofer_conflicto(self):
        """Prueba que al modificar un chofer entre en conflicto"""
        self.mockeamos_login_correcto()
        ClientController._get_ref_client = mock.MagicMock(return_value='ref')
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 3,
            'message': 'conflictos de colision'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(409)
        SharedServer.put_client = MagicMock(return_value=response_mock)
        payload = '{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}'
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put(
            '/api/v1/driver/14', data=payload, headers=headers)
        assert_res = json.loads("""{
            "code": 3,
            "message": "conflictos de colision"
        }""")
        self.assertEqual(response.status_code, 409)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    #Pruebas de cliente

    #Get cliente

    def test_obtener_cliente(self):
        """Prueba que al obtener un cliente este sea igual al que viene por defecto"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': '1'
            },
            'user': {
                'id': 'c1',
                '_ref': '2werwerfw',
                'applicationOwner': 'string',
                'type': 'passenger',
                'cars': [
                    {
                        'id': '1',
                        '_ref': 'erge',
                        'owner': 'c1',
                        'properties': [
                            {
                                'name': 'color',
                                'value': 'negro'
                            },
                            {
                                'name': 'marca',
                                'value': 'fiat'
                            }
                        ]
                    }
                ],
                'username': 'mz',
                'name': 'martin',
                'surname': 'tincho',
                'country': 'argentina',
                'email': 'm.t@gmail.com',
                'birthdate': '12/12/2000',
                'images': [
                    'http://sdfpsdf.com/sfisdjfoosi.jpg'
                ],
                'balance': [
                    {
                        'currency': 'peso',
                        'value': 200
                    }
                ]
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/client/23')
        assert_res = json.loads("""{
            "id": "c1",
            "_ref": "2werwerfw",
            "applicationOwner": "string",
            "type": "passenger",
            "cars": [
                {
                "id": "1",
                "_ref": "erge",
                "owner": "c1",
                "properties": [
                    {
                    "name": "color",
                    "value": "negro"
                    },
                    {
                    "name": "marca",
                    "value": "fiat"
                    }
                ]
                }
            ],
            "username": "mz",
            "name": "martin",
            "surname": "tincho",
            "country": "argentina",
            "email": "m.t@gmail.com",
            "birthdate": "12/12/2000",
            "images": [
                "http://sdfpsdf.com/sfisdjfoosi.jpg"
            ],
            "balance": [
                {
                "currency": "peso",
                "value": 200
                }]
        }""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_cliente_no_autorizado(self):
        """Prueba que al obtener un cliente cuando no esta autorizado"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 1,
            'message': 'No esta autorizado a obtener la info del usuario'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(401)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/client/23')
        assert_res = json.loads("""{
            "code": 1,
            "message": "No esta autorizado a obtener la info del usuario"
        }""")
        self.assertEqual(response.status_code, 401)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_cliente_no_existe(self):
        """Prueba que al obtener un cliente cuando no existe"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 2,
            'message': 'No existe el usuario'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(404)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/client/23')
        assert_res = json.loads("""{
            "code": 2,
            "message": "No existe el usuario"
        }""")
        self.assertEqual(response.status_code, 404)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    #Get clientes

    def test_obtener_clientes(self):
        """Prueba que al obtener todos los clientes, viene el default"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'count': 2,
                'total': 2,
                'next': 'string',
                'prev': 'string',
                'first': 'string',
                'last': 'string',
                'version': 'string'
            },
            'users': [
                {
                    'id': 'c1',
                    '_ref': '2werwerfw',
                    'applicationOwner': 'string',
                    'type': 'passenger',
                    'cars': [
                        {
                            'id': '1',
                            '_ref': 'erge',
                            'owner': 'c1',
                            'properties': [{
                                    'name': 'color',
                                    'value': 'negro'
                                },
                                {
                                    'name': 'marca',
                                    'value': 'fiat'
                                }
                            ]
                        }
                    ],
                    'username': 'mz',
                    'name': 'martin',
                    'surname': 'tincho',
                    'country': 'argentina',
                    'email': 'm.t@gmail.com',
                    'birthdate': '12/12/2000',
                    'images': [
                        'http://sdfpsdf.com/sfisdjfoosi.jpg'
                    ],
                    'balance': [
                        {
                            'currency': 'peso',
                            'value': 200
                        },
                        {
                            'id': 'c2',
                            '_ref': '2werwedrfw',
                            'applicationOwner': 'string',
                            'type': 'passenger',
                            'cars': [
                                {
                                    'id': '1',
                                    '_ref': 'erge',
                                    'owner': 'c1',
                                    'properties': [
                                        {
                                            'name': 'color',
                                            'value': 'rojo'
                                        },
                                        {
                                            'name': 'marca',
                                            'value': 'fiat'
                                        }
                                    ]
                                }
                            ],
                            'username': 'ht',
                            'name': 'homero',
                            'surname': 'simpson',
                            'country': 'argentina',
                            'email': 'h.t@gmail.com',
                            'birthdate': '12/05/1970',
                            'images': [
                                'http://sdfpsdf.com/aaaaaaosi.jpg'
                            ],
                            'balance': [
                                {
                                    'currency': 'peso',
                                    'value': 9000
                                }
                            ]
                        }
                    ]
                }
            ]
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_clients = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/clients')
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""[{
            "id": "c1",
            "_ref": "2werwerfw",
            "applicationOwner": "string",
            "type": "passenger",
            "cars": [{
                "id": "1",
                "_ref": "erge",
                "owner": "c1",
                "properties": [{
                        "name": "color",
                        "value": "negro"
                    },
                    {
                        "name": "marca",
                        "value": "fiat"
                    }
                ]
            }],
            "username": "mz",
            "name": "martin",
            "surname": "tincho",
            "country": "argentina",
            "email": "m.t@gmail.com",
            "birthdate": "12/12/2000",
            "images": [
                "http://sdfpsdf.com/sfisdjfoosi.jpg"
            ],
            "balance": [{
                    "currency": "peso",
                    "value": 200
                },
                {
                    "id": "c2",
                    "_ref": "2werwedrfw",
                    "applicationOwner": "string",
                    "type": "passenger",
                    "cars": [{
                        "id": "1",
                        "_ref": "erge",
                        "owner": "c1",
                        "properties": [{
                                "name": "color",
                                "value": "rojo"
                            },
                            {
                                "name": "marca",
                                "value": "fiat"
                            }
                        ]
                    }],
                    "username": "ht",
                    "name": "homero",
                    "surname": "simpson",
                    "country": "argentina",
                    "email": "h.t@gmail.com",
                    "birthdate": "12/05/1970",
                    "images": [
                        "http://sdfpsdf.com/aaaaaaosi.jpg"
                    ],
                    "balance": [{
                        "currency": "peso",
                        "value": 9000
                    }]
                }
            ]
        }]""")
        self.assertEqual(response.status_code, 200)
        self.assertEqual.__self__.maxDiff = None
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_clientes_desautorizado(self):
        """Prueba que al obtener todos los clientes sin autorizacion"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 3,
            'message': 'No estas autorizado'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(401)
        SharedServer.get_clients = MagicMock(return_value=response_mock)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/clients')
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 3,
            "message": "No estas autorizado"
        }""")
        self.assertEqual(response.status_code, 401)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    #Post cliente

    def test_crear_cliente(self):
        """Prueba que al crear un cliente con la informacion valida entonces devuelva
           un mensaje que se creo correctamente"""
        self.mockeamos_login_correcto()
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
         #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'xx'
            },
            'user': {
                'id': 'c1',
                '_ref': '2werwerfw',
                'applicationOwner': 'string',
                'type': 'passenger',
                'cars': [{
                    'id': '1',
                    '_ref': 'erge',
                    'owner': 'c1',
                    'properties': [{
                        'name': 'color',
                        'value': 'negro'
                    },
                    {
                        'name': 'marca',
                        'value': 'fiat'
                    }]
                }],
                'username': 'mz',
                'name': 'martin',
                'surname': 'tincho',
                'country': 'argentina',
                'email': 'm.t@gmail.com',
                'birthdate': '12/12/2000',
                'images': [
                    'http://sdfpsdf.com/sfisdjfoosi.jpg'
                ],
                'balance': [{
                    'currency': 'peso',
                    'value': 200
                }]
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(201)
        SharedServer.post_client = MagicMock(return_value=response_mock)
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        response = self.app.post('/api/v1/client', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "id": "c1",
            "_ref": "2werwerfw",
            "applicationOwner": "string",
            "type": "passenger",
            "cars": [{
                "id": "1",
                "_ref": "erge",
                "owner": "c1",
                "properties": [{
                    "name": "color",
                    "value": "negro"
                },
                {
                "name": "marca",
                "value": "fiat"
                }]
            }],
            "username": "mz",
            "name": "martin",
            "surname": "tincho",
            "country": "argentina",
            "email": "m.t@gmail.com",
            "birthdate": "12/12/2000",
            "images": [
                "http://sdfpsdf.com/sfisdjfoosi.jpg"
            ],
            "balance": [{
                "currency": "peso",
                "value": 200
            }]
        }""")
        self.assertEqual(response.status_code, 201)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_crear_cliente_insuficientes_parametros(self):
        """Prueba que al crear un cliente con falta de informacion"""
        self.mockeamos_login_correcto()
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 1,
            'message': 'No se cumplio con las precondiciones'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(400)
        SharedServer.post_client = MagicMock(return_value=response_mock)
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.add_usuario = MagicMock(return_value=True)
        response = self.app.post('/api/v1/client', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 1,
            "message": "No se cumplio con las precondiciones"
        }""")
        self.assertEqual(response.status_code, 400)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_crear_cliente_sin_informacion(self):
        """Prueba que al crear un cliente sin mandar la informacion devuelva el codigo de
           error correspondiente"""
        self.mockeamos_login_correcto()
        payload = ''
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.post(
            '/api/v1/client', data=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

    #Put cliente

    def test_modificar_cliente(self):
        """Prueba que al modificar un cliente con la informacion valida entonces devuelve
           un mensaje que se creo correctamente"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ClientController._get_ref_client = mock.MagicMock(return_value='ref')
        ModelManager.get_info_usuario = MagicMock(return_value={})
        ModelManager.update_usuario = mock.MagicMock(return_value=True)
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': '1'
            },
            'user': {
                'id': 'c1',
                '_ref': '2werwerfw',
                'applicationOwner': 'string',
                'type': 'passenger',
                'cars': [
                    {
                        'id': '1',
                        '_ref': 'erge',
                        'owner': 'c1',
                        'properties': [
                            {
                                'name': 'color',
                                'value': 'negro'
                            },
                            {
                                'name': 'marca',
                                'value': 'fiat'
                            }
                        ]
                    }
                ],
                'username': 'mz',
                'name': 'martin',
                'surname': 'tincho',
                'country': 'argentina',
                'email': 'm.t@gmail.com',
                'birthdate': '12/12/2000',
                'images': [
                    'http://sdfpsdf.com/sfisdjfoosi.jpg'
                ],
                'balance': [
                    {
                        'currency': 'peso',
                        'value': 200
                    }
                ]
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(201)
        ModelManager.get_info_usuario = MagicMock(return_value={})
        ModelManager.update_usuario = MagicMock(return_value=True)
        SharedServer.put_client = MagicMock(return_value=response_mock)
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put(
            '/api/v1/client/88', data=payload, headers=headers)
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "id": "c1",
            "_ref": "2werwerfw",
            "applicationOwner": "string",
            "type": "passenger",
            "cars": [
                {
                    "id": "1",
                    "_ref": "erge",
                    "owner": "c1",
                    "properties": [
                        {
                            "name": "color",
                            "value": "negro"
                        },
                        {
                            "name": "marca",
                            "value": "fiat"
                        }
                    ]
                }
            ],
            "username": "mz",
            "name": "martin",
            "surname": "tincho",
            "country": "argentina",
            "email": "m.t@gmail.com",
            "birthdate": "12/12/2000",
            "images": [
                "http://sdfpsdf.com/sfisdjfoosi.jpg"
            ],
            "balance": [
                {
                    "currency": "peso",
                    "value": 200
                }
            ]
        }""")
        self.assertEqual(response.status_code, 201)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_modificar_cliente_sin_informacion(self):
        """Prueba que al modificar un cliente sin mandar la informacion devuelva el codigo de
           error correspondiente"""
        self.mockeamos_login_correcto()
        ClientController._get_ref_client = mock.MagicMock(return_value='ref')
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 1,
            'message': 'No se cumplio con las precondiciones'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(400)
        SharedServer.put_client = MagicMock(return_value=response_mock)
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put(
            '/api/v1/client/14', data=payload, headers=headers)
        assert_res = json.loads("""{
            "code": 1,
            "message": "No se cumplio con las precondiciones"
        }""")
        self.assertEqual(response.status_code, 400)
        cmp_response = json.loads(response.data.decode('utf-8'))
        print(response.data)
        self.assertEqual(assert_res, cmp_response)

    def test_modificar_cliente_no_existe(self):
        """Prueba que al modificar un cliente que no existe"""
        self.mockeamos_login_correcto()
        ClientController._get_ref_client = mock.MagicMock(return_value='ref')
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 2,
            'message': 'No existe el usuario'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(404)
        SharedServer.put_client = MagicMock(return_value=response_mock)
        payload = '{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}'
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put(
            '/api/v1/client/14', data=payload, headers=headers)
        assert_res = json.loads("""{
            "code": 2,
            "message": "No existe el usuario"
        }""")
        self.assertEqual(response.status_code, 404)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_modificar_cliente_conflicto(self):
        """Prueba que al modificar un cliente entre en conflicto"""
        self.mockeamos_login_correcto()
        ClientController._get_ref_client = mock.MagicMock(return_value='ref')
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 3,
            'message': 'conflictos de colision'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(409)
        SharedServer.put_client = MagicMock(return_value=response_mock)
        payload = '{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}'
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put(
            '/api/v1/client/14', data=payload, headers=headers)
        assert_res = json.loads("""{
            "code": 3,
            "message": "conflictos de colision"
        }""")
        self.assertEqual(response.status_code, 409)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    #Delete cliente

    def test_eliminar_clienteww(self):
        """Prueba eliminar un chofer"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 'ok'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(204)
        SharedServer.delete_client = MagicMock(return_value=response_mock)
        ModelManager.delete_usuario = MagicMock(return_value=True)
        response = self.app.delete('/api/v1/client/23')
        self.assertEqual(response.status_code, 204)

    def test_eliminar_cliente_no_autorizado(self):
        """Prueba eliminar un chofer cuando no esta autorizado"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 1,
            'message': 'No esta autorizado a eliminar el usuario'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(401)
        SharedServer.delete_client = MagicMock(return_value=response_mock)
        response = self.app.delete('/api/v1/client/23')
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 1,
            "message": "No esta autorizado a eliminar el usuario"
        }""")
        self.assertEqual(response.status_code, 401)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_eliminar_cliente_no_existente(self):
        """Prueba eliminar un chofer que no existe"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 2,
            'message': 'No existe el usuario'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(404)
        SharedServer.delete_client = MagicMock(return_value=response_mock)
        response = self.app.delete('/api/v1/client/23')
        #Adentro del loads hay que pegar el json que devuelve la url
        assert_res = json.loads("""{
            "code": 2,
            "message": "No existe el usuario"
        }""")
        self.assertEqual(response.status_code, 404)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    # Test de autos

    def test_obtener_auto_cliente(self):
        """Prueba obtener un auto correctamente"""
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'xx'
            },
            'car':{
                'id': '2',
                '_ref': 'fgsssdf2',
                'owner': '23',
                'properties': [
                    {
                        'name': 'color',
                        'value': 'negro'
                    },
                    {
                        'name': 'marca',
                        'value': 'toyota'
                    }
                ]
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_car = MagicMock(return_value=response_mock)
        ClientController._get_ref_car = mock.MagicMock(return_value='ref')
        ClientController._save_car_ref = mock.MagicMock(return_value=True)
        ClientController._delete_car_ref = mock.MagicMock(return_value=True)
        #Llamar a la API
        response = self.app.get('api/v1/driver/23/cars/1')
        self.assertEqual(response.status_code, 200)
        cmp_test = json.loads("""{
            "id": "2",
            "_ref": "fgsssdf2",
            "owner": "23",
            "properties": [
                {
                    "name": "color",
                    "value": "negro"
                },
                {
                    "name": "marca",
                    "value": "toyota"
                }
            ]
        }""")
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(cmp_test, cmp_response)

    # def test_obtener_auto_cliente_inexistente(self):
    #     """Prueba obtener un auto de un cliente inexistente"""
    #     self.mockeamos_login_correcto()
    #     ClientController._get_ref_car = mock.MagicMock(return_value='ref')
    #     ClientController._save_car_ref = mock.MagicMock(return_value=True)
    #     ClientController._delete_car_ref = mock.MagicMock(return_value=True)
    #     #Mock del response
    #     response_mock = ResponseMock()
    #     response_shared = json.dumps({
    #         'code': 1,
    #         'message': 'No existe el usuario'
    #     })
    #     response_mock.set_response(response_shared)
    #     response_mock.set_code(404)
    #     response = self.app.get('/api/v1/driver/0/cars/1')
    #     self.assertEqual(response.status_code, 404)
    #     cmp_test = json.loads("""
    #     {
    #         "code": 1,
    #         "message": "No existe el usuario"
    #     }
    #     """)
    #     cmp_response = json.loads(response.data)
    #     self.assertEqual(cmp_test, cmp_response)

    def test_obtener_auto_inexistente(self):
        """Prueba obtener un auto que no tiene el cliente"""
        self.mockeamos_login_correcto()
        ClientController._get_ref_car = mock.MagicMock(return_value='ref')
        ClientController._save_car_ref = mock.MagicMock(return_value=True)
        ClientController._delete_car_ref = mock.MagicMock(return_value=True)
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 1,
            'message': 'No existe el auto'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(404)
        SharedServer.get_car = mock.MagicMock(return_value=response_mock)
        response = self.app.get('/api/v1/driver/23/cars/99')
        self.assertEqual(response.status_code, 404)
        cmp_test = json.loads("""
        {
            "code": 1,
            "message": "No existe el auto"
        }
        """)
        cmp_response = json.loads(response.data)
        self.assertEqual(cmp_test, cmp_response)

    def test_crear_auto_cliente(self):
        """Prueba crear un auto correctamente"""
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'xx'
            },
            'car':{
                'id': '2',
                '_ref': 'fgsssdf2',
                'owner': '23',
                'properties': [
                    {
                        'name': 'color',
                        'value': 'negro'
                    },
                    {
                        'name': 'marca',
                        'value': 'toyota'
                    }
                ]
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.post_car = MagicMock(return_value=response_mock)
        ClientController._get_ref_car = mock.MagicMock(return_value='ref')
        ClientController._save_car_ref = mock.MagicMock(return_value=True)
        ClientController._delete_car_ref = mock.MagicMock(return_value=True)
        #Llamar a la API
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.post(
            '/api/v1/driver/23/cars', data=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        cmp_test = json.loads("""{
            "id": "2",
            "_ref": "fgsssdf2",
            "owner": "23",
            "properties": [
                {
                    "name": "color",
                    "value": "negro"
                },
                {
                    "name": "marca",
                    "value": "toyota"
                }
            ]
        }""")
        self.assertEqual(cmp_test, cmp_response)

    def test_crear_auto_cliente_sin_propiedades(self):
        """Prueba crear un auto sin propiedades"""
        self.mockeamos_login_correcto()
        payload = '{}'
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        ClientController._get_ref_car = mock.MagicMock(return_value='ref')
        ClientController._save_car_ref = mock.MagicMock(return_value=True)
        ClientController._delete_car_ref = mock.MagicMock(return_value=True)
        response = self.app.post(
            '/api/v1/driver/23/cars', data=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_modificar_auto_cliente(self):
        """Prueba modificar un auto correctamente"""
        self.mockeamos_login_correcto()
        ClientController._get_ref_client = mock.MagicMock(return_value='ref')
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'xx'
            },
            'car':{
                'id': '2',
                '_ref': 'fgsssdf2',
                'owner': '23',
                'properties': [
                    {
                        'name': 'color',
                        'value': 'negro'
                    },
                    {
                        'name': 'marca',
                        'value': 'toyota'
                    }
                ]
            }
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(201)
        SharedServer.put_car = MagicMock(return_value=response_mock)
        ClientController._get_ref_car = mock.MagicMock(return_value='ref')
        ClientController._save_car_ref = mock.MagicMock(return_value=True)
        ClientController._delete_car_ref = mock.MagicMock(return_value=True)
        #Llamo a la API
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put(
            '/api/v1/driver/23/cars/45', data=payload, headers=headers)
        print(str(response.data))
        self.assertEqual(response.status_code, 201)
        cmp_response = json.loads(response.data.decode('utf-8'))
        cmp_test = json.loads("""{
            "id": "2",
            "_ref": "fgsssdf2",
            "owner": "23",
            "properties": [
                {
                    "name": "color",
                    "value": "negro"
                },
                {
                    "name": "marca",
                    "value": "toyota"
                }
            ]
        }""")
        self.assertEqual(cmp_test, cmp_response)

    def test_modificar_auto_cliente_sin_propiedades(self):
        """Prueba para modificar un auto sin propiedades"""
        self.mockeamos_login_correcto()
        payload = ''
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put(
            '/api/v1/driver/23/cars/45', data=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_eliminar_auto(self):
        """Prueba eliminar un auto de un chofer"""
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({})
        response_mock.set_response(response_shared)
        response_mock.set_code(204)
        SharedServer.delete_car = MagicMock(return_value=response_mock)
        ClientController._get_ref_car = mock.MagicMock(return_value='ref')
        ClientController._save_car_ref = mock.MagicMock(return_value=True)
        ClientController._delete_car_ref = mock.MagicMock(return_value=True)
        response = self.app.delete('/api/v1/driver/23/cars/45')
        self.assertEqual(response.status_code, 204)

    def test_get_all_cars(self):
        """Prueba obtener todos los autos"""
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'xx'
            },
            'cars': [
                {
                    '_ref': 'fgdf2',
                    'id': '1',
                    'owner': '23',
                    'properties':[
                        {
                            'name': 'color',
                            'value': 'gris'
                        },
                        {
                            'name': 'marca',
                            'value': 'fiat'
                        }
                    ]
                },
                {
                    '_ref': 'fgsssdf2',
                    'id': '2',
                    'owner': '23',
                    'properties': [
                        {
                            'name': 'color',
                            'value': 'negro'
                        },
                        {
                            'name': 'marca',
                            'value': 'toyota'
                        }
                    ]
                }
            ]
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(200)
        SharedServer.get_cars = MagicMock(return_value=response_mock)
        #Llamamos a la API
        response = self.app.get('/api/v1/driver/23/cars')
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        assert_res = json.loads("""	[
                {
                    "_ref": "fgdf2",
                    "id": "1",
                    "owner": "23",
                    "properties":[
                        {
                            "name": "color",
                            "value": "gris"
                        },
                        {
                            "name": "marca",
                            "value": "fiat"
                        }
                    ]
                },
                {
                    "_ref": "fgsssdf2",
                    "id": "2",
                    "owner": "23",
                    "properties": [
                        {
                            "name": "color",
                            "value": "negro"
                        },
                        {
                            "name": "marca",
                            "value": "toyota"
                        }
                    ]
                }
            ]
        """)
        self.assertEqual(assert_res, cmp_response)

    #Test de choferes cercanos

    def test_obtener_informacion_choferes_cercanos(self):
        """Prueba obtener los choferes cercanos cuando existe un usuario cerca"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock de la respuesta de la base de datos al pedir los choferes
        ModelManager.get_started_and_unfinished_trips_with_driver_id = MagicMock(return_value=[])
        list_locations = [
            {
                "client_id": "1",
                "lat": "-34.619996",
                "long": "-58.686680"
            }
        ]
        ModelManager.get_locations_by_type = MagicMock(return_value=list_locations)
        #Mock del response los get de clientes de SharedServer
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'user': {
                'id': '23',
                '_ref': 'string',
                'applicationOwner': 'string',
                'type': 'chofer',
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
        ModelManager.user_is_available = MagicMock(return_value=True)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/closestdrivers/latitude/-34.619996/length/-58.686680/radio/1')
        assert_res = json.loads("""
        [
            {
                "info": {
                    "id": "23",
                    "_ref": "string",
                    "applicationOwner": "string",
                    "type": "chofer",
                    "cars": [
                        {
                            "id": "string",
                            "_ref": "string",
                            "owner": "string",
                            "properties": [
                                {
                                    "name": "string",
                                    "value": "string"
                                }
                            ]
                        }
                    ],
                    "username": "Khaleesi",
                    "name": "Daenerys",
                    "surname": "Targaryen",
                    "country": "Valyria",
                    "email": "madre_dragones@got.com",
                    "birthdate": "01/01/1990",
                    "images": [
                        "string"
                    ],
                    "balance": [
                        {
                            "currency": "string",
                            "value": 0
                        }
                    ]
                },
                "location": {
                    "client_id": "1",
                    "lat": "-34.619996",
                    "long": "-58.686680"
                }
            }
        ]""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_informacion_choferes_cercanos2(self):
        """Prueba obtener los choferes cercanos cuando existe un usuario cerca y otro usuario lejos"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_started_and_unfinished_trips_with_driver_id = MagicMock(return_value=[])
        #Mock de la respuesta de la base de datos al pedir los choferes
        list_locations = [
            {
                "client_id": "1",
                "lat": "-34.619996",
                "long": "-58.686680"
            },
            {
                "client_id": "2",
                "lat": "-44.619996",
                "long": "-48.686680"
            }
        ]
        ModelManager.get_locations_by_type = MagicMock(return_value=list_locations)
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.user_is_available = MagicMock(return_value=True)
        #Mock del response los get de clientes de SharedServer
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'user': {
                'id': '23',
                '_ref': 'string',
                'applicationOwner': 'string',
                'type': 'chofer',
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
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/closestdrivers/latitude/-34.619996/length/-58.686680/radio/1')
        assert_res = json.loads("""
        [
            {
                "info": {
                    "id": "23",
                    "_ref": "string",
                    "applicationOwner": "string",
                    "type": "chofer",
                    "cars": [
                        {
                            "id": "string",
                            "_ref": "string",
                            "owner": "string",
                            "properties": [
                                {
                                    "name": "string",
                                    "value": "string"
                                }
                            ]
                        }
                    ],
                    "username": "Khaleesi",
                    "name": "Daenerys",
                    "surname": "Targaryen",
                    "country": "Valyria",
                    "email": "madre_dragones@got.com",
                    "birthdate": "01/01/1990",
                    "images": [
                        "string"
                    ],
                    "balance": [
                        {
                            "currency": "string",
                            "value": 0
                        }
                    ]
                },
                "location": {
                    "client_id": "1",
                    "lat": "-34.619996",
                    "long": "-58.686680"
                }
            }
        ]""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_informacion_choferes_cercanos3(self):
        """Prueba obtener los choferes cercanos cuando existe dos usuario cerca y otro usuario lejos"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_started_and_unfinished_trips_with_driver_id = MagicMock(return_value=[])
        #Mock de la respuesta de la base de datos al pedir los choferes
        ModelManager.user_is_available = MagicMock(return_value=True)
        list_locations = [
            {
                "client_id": "1",
                "lat": "-34.619996",
                "long": "-58.686680"
            },
            {
                "client_id": "2",
                "lat": "-34.619996",
                "long": "-58.686680"
            },
            {
                "client_id": "3",
                "lat": "-44.619996",
                "long": "-48.686680"
            }
        ]
        ModelManager.get_locations_by_type = MagicMock(return_value=list_locations)
        #Mock del response los get de clientes de SharedServer
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'user': {
                'id': '23',
                '_ref': 'string',
                'applicationOwner': 'string',
                'type': 'chofer',
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
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/closestdrivers/latitude/-34.619996/length/-58.686680/radio/1')
        assert_res = json.loads("""
            [
                {
                    "info": {
                        "id": "23",
                        "_ref": "string",
                        "applicationOwner": "string",
                        "type": "chofer",
                        "cars": [
                        {
                            "id": "string",
                            "_ref": "string",
                            "owner": "string",
                            "properties": [
                            {
                                "name": "string",
                                "value": "string"
                            }
                            ]
                        }
                        ],
                        "username": "Khaleesi",
                        "name": "Daenerys",
                        "surname": "Targaryen",
                        "country": "Valyria",
                        "email": "madre_dragones@got.com",
                        "birthdate": "01/01/1990",
                        "images": [
                        "string"
                        ],
                        "balance": [
                        {
                            "currency": "string",
                            "value": 0
                        }
                        ]
                    },
                "location" : {
                    "client_id": "1",
                    "lat": "-34.619996",
                    "long": "-58.686680"
                }
            },
            {
                "info": {
                    "id": "23",
                    "_ref": "string",
                    "applicationOwner": "string",
                    "type": "chofer",
                    "cars": [
                        {
                            "id": "string",
                            "_ref": "string",
                            "owner": "string",
                            "properties": [
                            {
                                "name": "string",
                                "value": "string"
                            }
                            ]
                        }
                    ],
                    "username": "Khaleesi",
                    "name": "Daenerys",
                    "surname": "Targaryen",
                    "country": "Valyria",
                    "email": "madre_dragones@got.com",
                    "birthdate": "01/01/1990",
                    "images": [
                        "string"
                    ],
                    "balance": [
                        {
                            "currency": "string",
                            "value": 0
                        }
                    ]
                },
                "location": {
                    "client_id": "2",
                    "lat": "-34.619996",
                    "long": "-58.686680"
                }
            }
        ]""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_informacion_choferes_cercanos_no_disponibles(self):
        """Prueba obtener los choferes cercanos cuando existe dos usuario cerca y otro usuario lejos
           pero ninguno esta disponible"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_started_and_unfinished_trips_with_driver_id = MagicMock(return_value=[])
        #Mock de la respuesta de la base de datos al pedir los choferes
        ModelManager.user_is_available = MagicMock(return_value=False)
        list_locations = [
            {
                "client_id": "1",
                "lat": "-34.619996",
                "long": "-58.686680"
            },
            {
                "client_id": "2",
                "lat": "-34.619996",
                "long": "-58.686680"
            },
            {
                "client_id": "3",
                "lat": "-44.619996",
                "long": "-48.686680"
            }
        ]
        ModelManager.get_locations_by_type = MagicMock(return_value=list_locations)
        #Mock del response los get de clientes de SharedServer
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'user': {
                'id': '23',
                '_ref': 'string',
                'applicationOwner': 'string',
                'type': 'chofer',
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
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/closestdrivers/latitude/-34.619996/length/-58.686680/radio/1')
        assert_res = json.loads("""[ ]""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_informacion_choferes_cercanos_pero_no_hay_choferes_cercanos(self):
        """Prueba obtener los choferes cercanos cuando existe usuarios lejos"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_started_and_unfinished_trips_with_driver_id = MagicMock(return_value=[])
        #Mock de la respuesta de la base de datos al pedir los choferes
        ModelManager.user_is_available = MagicMock(return_value=True)
        list_locations = [
            {
                "client_id": "1",
                "lat": "-54.619996",
                "long": "-58.686680"
            },
            {
                "client_id": "2",
                "lat": "-44.619996",
                "long": "-48.686680"
            }
        ]
        ModelManager.get_locations_by_type = MagicMock(return_value=list_locations)
        #Mock del response los get de clientes de SharedServer
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'user': {
                'id': '23',
                '_ref': 'string',
                'applicationOwner': 'string',
                'type': 'chofer',
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
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/closestdrivers/latitude/-34.619996/length/-58.686680/radio/1')
        assert_res = json.loads("""
        []""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_informacion_choferes_cercanos_pero_no_hay_choferes(self):
        """Prueba obtener los choferes cercanos cuando existe usuarios lejos"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_started_and_unfinished_trips_with_driver_id = MagicMock(return_value=[])
        #Mock de la respuesta de la base de datos al pedir los choferes
        list_locations = []
        ModelManager.get_locations_by_type = MagicMock(return_value=list_locations)
        #Mock del response los get de clientes de SharedServer
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
            },
            'user': {
                'id': '23',
                '_ref': 'string',
                'applicationOwner': 'string',
                'type': 'chofer',
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
        ModelManager.user_is_available = MagicMock(return_value=True)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/closestdrivers/latitude/-34.619996/length/-58.686680/radio/1')
        assert_res = json.loads("""
        []""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_informacion_choferes_cercanos_con_usuario_inexistente(self):
        """Prueba obtener los choferes cercanos cuando existe un usuario cerca"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_started_and_unfinished_trips_with_driver_id = MagicMock(return_value=[])
        #Mock de la respuesta de la base de datos al pedir los choferes
        list_locations = [
            {
                "client_id": "1",
                "lat": "-34.619996",
                "long": "-58.686680"
            }
        ]
        ModelManager.get_locations_by_type = MagicMock(return_value=list_locations)
        #Mock del response los get de clientes de SharedServer
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 2,
            'message': 'No existe el usuario'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(404)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        ModelManager.user_is_available = MagicMock(return_value=True)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/closestdrivers/latitude/-34.619996/length/-58.686680/radio/1')
        assert_res = json.loads("""[]""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_obtener_informacion_choferes_cercanos_con_usuario_no_autorizado(self):
        """Prueba obtener los choferes cercanos cuando existe un usuario cerca"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_started_and_unfinished_trips_with_driver_id = MagicMock(return_value=[])
        #Mock de la respuesta de la base de datos al pedir los choferes
        list_locations = [
            {
                "client_id": "1",
                "lat": "-34.619996",
                "long": "-58.686680"
            }
        ]
        ModelManager.get_locations_by_type = MagicMock(return_value=list_locations)
        #Mock del response los get de clientes de SharedServer
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 1,
            'message': 'No esta autorizado a obtener la info del usuario'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(401)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        ModelManager.user_is_available = MagicMock(return_value=True)
        #Hacemos la llamada normal
        response = self.app.get('/api/v1/closestdrivers/latitude/-34.619996/length/-58.686680/radio/1')
        assert_res = json.loads("""[]""")
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    # Put disponibilidad del chofer

    def test_disponible_chofer(self):
        """Prueba poner disponible a un chofer"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.get_info_usuario = MagicMock(return_value={
            "client_type": "driver"
        })
        ModelManager.change_available_driver = MagicMock(return_value=True)
        #Hacemos la llamada normal
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put('/api/v1/driver/23/available', data=payload, headers=headers)
        assert_res = json.loads("""{
            "code": 0, 
            "message": "El chofer 23 ya se encuentra disponible."
        }""")
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 201)

    def test_disponible_chofer_sin_info(self):
        """Prueba poner disponible a un chofer que no se encuentra en la base de datos"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.add_usuario = MagicMock(return_value=True)
        #Mock del response los get de clientes de SharedServer
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
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.change_available_driver = MagicMock(return_value=True)
        #Hacemos la llamada normal
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put('/api/v1/driver/23/available', data=payload, headers=headers)
        assert_res = json.loads("""{
            "code": 0, 
            "message": "El chofer 23 ya se encuentra disponible."
        }""")
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 201)

    def test_disponible_chofer_no_chofer(self):
        """Prueba poner disponible a un chofer que no es un chofer"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value={
            "client_type": "passenger"
        })
        ModelManager.change_available_driver = MagicMock(return_value=True)
        #Hacemos la llamada normal
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put('/api/v1/driver/23/available', data=payload, headers=headers)
        assert_res = json.loads("""{
            "code": -11, 
            "message": "El usuario 23 no es un chofer."
        }""")
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 400)

    def test_disponible_chofer_sin_info_no_chofer(self):
        """Prueba poner disponible a un chofer que no se encuentra en la base de datos y
           al buscarlo nos damos cuenta que no es un chofer"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response los get de clientes de SharedServer
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
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.change_available_driver = MagicMock(return_value=True)
        ModelManager.add_usuario = MagicMock(return_value=True)
        #Hacemos la llamada normal
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put('/api/v1/driver/23/available', data=payload, headers=headers)
        assert_res = json.loads("""{
            "code": -11, 
            "message": "El usuario 23 no es un chofer."
        }""")
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 400)

    def test_disponible_chofer_no_existe(self):
        """Prueba poner disponible a un chofer que no se encuentra en la base de datos y
           al buscarlo nos damos cuenta que no es un chofer"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response los get de clientes de SharedServer
        ModelManager.add_usuario = MagicMock(return_value=True)
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 2,
            'message': 'No existe el usuario'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(404)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.change_available_driver = MagicMock(return_value=True)
        #Hacemos la llamada normal
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put('/api/v1/driver/23/available', data=payload, headers=headers)
        assert_res = json.loads("""{
            "code": -10, 
            "message": "El usuario 23 no existe."
        }""")
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 404)

    # Put no disponible chofer

    def test_no_disponible_chofer(self):
        """Prueba poner disponible a un chofer"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.add_usuario = MagicMock(return_value=True)
        ModelManager.get_info_usuario = MagicMock(return_value={
            "client_type": "driver"
        })
        ModelManager.change_available_driver = MagicMock(return_value=True)
        #Hacemos la llamada normal
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put('/api/v1/driver/23/unavailable', data=payload, headers=headers)
        assert_res = json.loads("""{
            "code": 0, 
            "message": "El chofer 23 ya no se encuentra disponible."
        }""")
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 201)

    def test_no_disponible_chofer_sin_info(self):
        """Prueba poner disponible a un chofer que no se encuentra en la base de datos"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.add_usuario = MagicMock(return_value=True)
        #Mock del response los get de clientes de SharedServer
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
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.change_available_driver = MagicMock(return_value=True)
        #Hacemos la llamada normal
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put('/api/v1/driver/23/unavailable', data=payload, headers=headers)
        assert_res = json.loads("""{
            "code": 0, 
            "message": "El chofer 23 ya no se encuentra disponible."
        }""")
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 201)

    def test_no_disponible_chofer_no_chofer(self):
        """Prueba poner disponible a un chofer que no es un chofer"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        ModelManager.get_info_usuario = MagicMock(return_value={
            "client_type": "passenger"
        })
        ModelManager.change_available_driver = MagicMock(return_value=True)
        #Hacemos la llamada normal
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put('/api/v1/driver/23/unavailable', data=payload, headers=headers)
        assert_res = json.loads("""{
            "code": -11, 
            "message": "El usuario 23 no es un chofer."
        }""")
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 400)

    def test_no_disponible_chofer_sin_info_no_chofer(self):
        """Prueba poner disponible a un chofer que no se encuentra en la base de datos y
           al buscarlo nos damos cuenta que no es un chofer"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response los get de clientes de SharedServer
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
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.change_available_driver = MagicMock(return_value=True)
        ModelManager.add_usuario = MagicMock(return_value=True)
        #Hacemos la llamada normal
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put('/api/v1/driver/23/unavailable', data=payload, headers=headers)
        assert_res = json.loads("""{
            "code": -11, 
            "message": "El usuario 23 no es un chofer."
        }""")
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 400)

    def test_no_disponible_chofer_no_existe(self):
        """Prueba poner disponible a un chofer que no se encuentra en la base de datos y
           al buscarlo nos damos cuenta que no es un chofer"""
        #Mockeamos la llamada
        self.mockeamos_login_correcto()
        #Mock del response los get de clientes de SharedServer
        ModelManager.add_usuario = MagicMock(return_value=True)
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'code': 2,
            'message': 'No existe el usuario'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(404)
        SharedServer.get_client = MagicMock(return_value=response_mock)
        ModelManager.get_info_usuario = MagicMock(return_value=None)
        ModelManager.change_available_driver = MagicMock(return_value=True)
        #Hacemos la llamada normal
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.put('/api/v1/driver/23/unavailable', data=payload, headers=headers)
        assert_res = json.loads("""{
            "code": -10, 
            "message": "El usuario 23 no existe."
        }""")
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)
        self.assertEqual(response.status_code, 404)
