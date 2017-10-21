""" @package test.client_shared_test
"""
import unittest
import mock
from service.login_service import LoginService
import json
import main_app
import requests
from mock import MagicMock
from service.shared_server import SharedServer
from api.client_controller import ClientController
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
        SharedServer._get_url = mock.MagicMock(return_value='http://llevamesharedserver.mocklab.io/users?token=tokenApiDriver')
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
            }]
        }""")
        self.assertEqual(response.status_code, 201)
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(assert_res, cmp_response)

    def test_crear_chofer_insuficientes_parametros(self):
        """Prueba que al crear un chofer con falta de informacion devuelva codigo de error de precondiciones"""
        self.mockeamos_login_correcto()
        payload = "{\r\n  \"username\": \"Khaleesi\",\r\n  \"password\": \"Dragones3\",\r\n  \"fb\": {\r\n    \"userId\": \"MadreDragones\",\r\n    \"authToken\": \"fb_auth_token\"\r\n  },\r\n  \"firstName\": \"Daenerys\",\r\n  \"lastName\": \"Targaryen\",\r\n  \"country\": \"Valyria\",\r\n  \"email\": \"madre_dragones@got.com\",\r\n  \"birthdate\": \"01/01/1990\",\r\n  \"images\": [\r\n    \"https://typeset-beta.imgix.net/rehost%2F2016%2F9%2F13%2F7c8791ae-a840-4637-9d89-256db36e8174.jpg\"\r\n  ]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        #Mockeamos la llamada
        SharedServer._get_url = mock.MagicMock(return_value='http://llevamesharedserver.mocklab.io/users?token=tokenApiDriverInsufParam')
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
        SharedServer._get_url = mock.MagicMock(return_value='http://llevamesharedserver.mocklab.io/users?token=tokenApi')
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
        SharedServer._get_url = mock.MagicMock(return_value='http://llevamesharedserver.mocklab.io/users/23/cars/1?token=tokenApi')
        response = self.app.get('api/v1/driver/23/cars/1')
        self.assertEqual(response.status_code, 200)
        cmp_test = json.loads("""{
                "car_id": "1",
                "owner": "23",
                "properties": [
                {
                    "name": "color",
                    "value": "negro"
                },
                {
                    "name": "modelo",
                    "value": "punto"
                },
                {
                    "name": "marca",
                    "value": "fiat"
                }]}""")
        cmp_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(cmp_test, cmp_response)

#    def test_obtener_auto_cliente_inexistente(self):
 #       """Prueba obtener un auto de un cliente inexistente"""
  #      self.mockeamos_login_correcto()
   #     response = self.app.get('/api/v1/driver/0/cars/1')
    #    self.assertEqual(response.status_code, 404)
     #   cmp_test = json.loads("""
      #  """)
       # cmp_response = json.loads(response.data)
        #self.assertEqual(cmp_test, cmp_response)

#    def test_obtener_auto_inexistente(self):
 #       """Prueba obtener un auto que no tiene el cliente"""
  #      self.mockeamos_login_correcto()
   #     response = self.app.get('/api/v1/driver/23/cars/99')
    #    self.assertEqual(response.status_code, 404)
     #   cmp_test = json.loads("""
      #  """)
       # cmp_response = json.loads(response.data)
        #self.assertEqual(cmp_test, cmp_response)

    def test_crear_auto_cliente(self):
        """Prueba crear un auto correctamente"""
        self.mockeamos_login_correcto()
        #Mock del response
        response_mock = ResponseMock()
        response_shared = json.dumps({
            'metadata': {
                'version': 'string'
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
        SharedServer.post_car = MagicMock(return_value=response_mock)
        payload = "{\r\n\t\"properties\": [\r\n\t\t{\r\n\t\t    \"name\": \"color\",\r\n\t\t    \"value\": \"negro\"\r\n\t\t},\r\n\t\t{\r\n\t\t    \"name\": \"modelo\",\r\n\t\t    \"value\": \"punto\"\r\n\t\t},\r\n\t\t{\r\n\t\t    \"name\": \"marca\",\r\n\t\t    \"value\": \"fiat\"\r\n\t\t}\r\n\t]\r\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
        response = self.app.post(
            '/api/v1/driver/23/cars', data=payload, headers=headers)
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

    def test_crear_auto_cliente_sin_propiedades(self):
        """Prueba crear un auto sin propiedades"""
        self.mockeamos_login_correcto()
        payload = ''
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "1795714f-644d-3186-bb79-f6bb4ba39f00"
        }
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
                'version': '1'
            },
            'car': {
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
        payload = "{\r\n\t\"properties\": [\r\n\t\t{\r\n\t\t    \"name\": \"color\",\r\n\t\t    \"value\": \"negro\"\r\n\t\t},\r\n\t\t{\r\n\t\t    \"name\": \"modelo\",\r\n\t\t    \"value\": \"punto\"\r\n\t\t},\r\n\t\t{\r\n\t\t    \"name\": \"marca\",\r\n\t\t    \"value\": \"fiat\"\r\n\t\t}\r\n\t]\r\n}"
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
        response_shared = json.dumps({
            'code': '0'
        })
        response_mock.set_response(response_shared)
        response_mock.set_code(204)
        SharedServer.delete_car = MagicMock(return_value=response_mock)
        response = self.app.delete('/api/v1/driver/23/cars/45')
        self.assertEqual(response.status_code, 204)

    def test_get_all_cars(self):
        """Prueba obtener todos los autos"""
        self.mockeamos_login_correcto()
        url = 'http://llevamesharedserver.mocklab.io/users/23/cars?token=tokenApi'
        SharedServer._get_url = mock.MagicMock(return_value=url)
        response = self.app.get('/api/v1/driver/23/cars')
        self.assertEqual(response.status_code, 200)
        cmp_response = json.loads(response.data.decode('utf-8'))
        cmp_test = json.loads(json.dumps([
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
        ]))
        self.assertEqual(cmp_test, cmp_response)
