""" @package main
"""
import os
from flask import Flask, jsonify, abort, make_response, request, session
from flasgger import Swagger
from flasgger.utils import swag_from
from api.client_controller import ClientController
from api.trip_controller import TripController
from api.client_controller import TIPO_CLIENTE
from api.client_controller import TIPO_CHOFER
from service.login_service import LoginService

#Para levantar swagger hay que ir a http://localhost:5000/apidocs/

application = Flask(__name__)

TRIP_CONTROLLER = TripController()
CLIENT_CONTROLLER = ClientController()
LOGIN_SERVICE = LoginService()

FALTA_LOGUEARSE = 'Falta loguearse'

#Secret key para las session
application.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

TEMPLATE_SWAGGER = {
    "swagger": "2.0",
    "info": {
        "title": "ApplicationServer",
        "description": "API para Llevame",
        "contact": {
            "responsibleOrganization": "Grupo 6"
        },
        "version": "1.0.0"
    },
    "basePath": "/",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ]
}

Swagger(application, template=TEMPLATE_SWAGGER)

@application.errorhandler(404)
def not_found():
    """Manejador de error para codigo 404"""
    application.logger.error('Error 404 - Recurso no encontrado')
    return make_response(jsonify({'error': 'Not Found'}), 404)

@application.route('/logtest')
def log_test():
    """Url para testing de logueo a distintos niveles"""
    application.logger.warning('Testeando Warning!')
    application.logger.error('Testeando Error!')
    application.logger.info('Testeando Info!')
    return "Testeando el Logger..."

#Seniales de vida
@application.route('/api/v1/keepalive', methods=['GET'])
def keepalive():
    """Damos seniales de vida"""
    application.logger.info('[GET] /api/v1/keepalive')
    response = jsonify(code='OK')
    response.status_code = 200
    return response

#Login y logout

def is_logged():
    """Verifica si esta logueado el usuario o no lo esta"""
    return LOGIN_SERVICE.is_logged(session)

@application.route('/login/facebookAuthToken/<string:facebook_auth_token>', methods=['GET', 'POST'])
def login_facebook(facebook_auth_token):
    """Logueamos al usuario
    @param facebookAuthToken es el token de facebook que tenemos guardado en el sistema"""
    if request.method == 'POST':
        application.logger.info('[POST] /login/facebookAuthToken/' + str(facebook_auth_token))
        if not facebook_auth_token:
            return make_response(jsonify({'respuesta': 'Credenciales invalidas'}), 401)
        return LOGIN_SERVICE.login_facebook(facebook_auth_token, session)
    return '''
        <form method="post">
            <p><input type=text name=estaSeguro>
            <p><input type=submit value=Login>
        </form>
    '''

@application.route('/login/username/<string:username>/password/<string:password>', methods=['GET', 'POST'])
def login(username, password):
    """Logueamos al usuario
    @param username es el nombre del usuario que guardo en el sistema
    @param password es la contraseña del usuario"""
    if request.method == 'POST':
        application.logger.info('[POST] /login/username/' + str(username) + '/password/' + str(password))
        if not (username and password):
            return make_response(jsonify({'respuesta': 'Credenciales invalidas'}), 401)
        return LOGIN_SERVICE.login(username, password, session)
    return '''
        <form method="post">
            <p><input type=text name=estaSeguro>
            <p><input type=submit value=Login>
        </form>
    '''

@application.route('/logout', methods=['POST', 'GET'])
def logout():
    """Deslogueamos al usuario"""
    application.logger.info('[POST] /logout')
    LOGIN_SERVICE.logout(session)
    response = jsonify(mensaje='Se deslogueo correctamente')
    response.status_code = 200
    return response

def response_invalid_login():
    """Devuelve el json con la respuesta que indica que el usuario no esta logueado o es invalido"""
    application.logger.info('No estaba logueado o estaba mal logueado')
    response = jsonify(mensaje=FALTA_LOGUEARSE)
    response.status_code = 401
    return response

#Endpoints de Choferes

@application.route('/api/v1/driver/<string:driver_id>', methods=['GET'])
def get_info_driver(driver_id):
    """Devuelve la informacion de un chofer
    @param driver_id es el identificador del chofer"""
    application.logger.info('[GET] /api/v1/driver/' + str(driver_id))
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    response = CLIENT_CONTROLLER.get_client(driver_id)
    return response

@application.route('/api/v1/drivers', methods=['GET'])
def get_info_drivers():
    """Devuelve la informacion de todos los choferes"""
    application.logger.info('[GET] /api/v1/drivers')
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    response = CLIENT_CONTROLLER.get_clients(TIPO_CHOFER)
    return response

@application.route('/api/v1/driver', methods=['POST'])
def post_info_driver():
    """Crea un nuevo chofer"""
    application.logger.info('[POST] /api/v1/driver')
    if not request.json:
        abort(400)
    response = CLIENT_CONTROLLER.post_new_client(request.json, TIPO_CHOFER)
    return response

@application.route('/api/v1/driver/<string:driver_id>', methods=['PUT'])
def put_info_driver(driver_id):
    """Modifica un chofer
    @param driver_id es el identificador del driver"""
    application.logger.info('[PUT] /api/v1/driver/' + str(driver_id))
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    if not request.json:
        abort(400)
    response = CLIENT_CONTROLLER.put_new_client(request.json, TIPO_CHOFER, driver_id)
    return response

#Endpoints de clientes

@application.route('/api/v1/client/<string:client_id>', methods=['GET'])
def get_info_client(client_id):
    """Devuelve la informacion de un cliente
    @param client_id es el identificador del cliente"""
    application.logger.info('[GET] /api/v1/client/' + str(client_id))
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    response = CLIENT_CONTROLLER.get_client(client_id)
    return response

@application.route('/api/v1/clients', methods=['GET'])
def get_info_clients():
    """Devuelve la informacion de todos los clientes"""
    application.logger.info('[GET] /api/v1/clients')
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    response = CLIENT_CONTROLLER.get_clients(TIPO_CLIENTE)
    return response

@application.route('/api/v1/client', methods=['POST'])
def post_info_client():
    """Crea un nuevo cliente"""
    application.logger.info('[POST] /api/v1/client')
    if not request.json:
        abort(400)
    response = CLIENT_CONTROLLER.post_new_client(request.json, TIPO_CLIENTE)
    return response

@application.route('/api/v1/client/<string:client_id>', methods=['PUT'])
def put_info_client(client_id):
    """Modificar un cliente
    @param client_id es el identificador del cliente"""
    application.logger.info('[PUT] /api/v1/client/' + str(client_id))
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    if not request.json:
        abort(400)
    response = CLIENT_CONTROLLER.put_new_client(request.json, TIPO_CLIENTE, client_id)
    return response

@application.route('/api/v1/client/<string:client_id>', methods=['DELETE'])
def delete_info_client(client_id):
    """Devuelve la informacion de un cliente
    @param client_id es el identificador del cliente"""
    application.logger.info('[DELETE] /api/v1/client/' + str(client_id))
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    response = CLIENT_CONTROLLER.delete_client(client_id)
    return response

# Endpoints de autos

@application.route('/api/v1/driver/<string:driver_id>/cars/<int:car_id>',methods=['GET'])
def get_info_car(driver_id, car_id):
    """Devuelve la informacion del auto de un conductor"""
    application.logger.info('[GET] /api/v1/driver/'+str(driver_id)+'/cars/' + str(car_id))
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    response = CLIENT_CONTROLLER.get_car(car_id, driver_id)
    return response

@application.route('/api/v1/driver/<string:driver_id>/cars', methods=['GET'])
def get_all_cars(driver_id):
    """Devuelve la informacion de todos los autos asociados a un conductor"""
    application.logger.info('[GET] /api/v1/driver/' + str(driver_id))
    #login check
    if not is_logged():
        return response_invalid_login()
    response = CLIENT_CONTROLLER.get_cars(driver_id)
    return response

@application.route('/api/v1/driver/<string:driver_id>/cars', methods=['POST'])
def post_info_car(driver_id):
    """Crea un nuevo auto para un chofer
    @param car_id es el identificador del auto de un chofer
    @param driver_id es el identificador del chofer"""
    application.logger.info('[POST] /api/v1/driver/'+str(driver_id)+'/cars')
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    if not request.json:
        abort(400)
    response = CLIENT_CONTROLLER.post_new_car(request.json, driver_id)
    return response

@application.route('/api/v1/driver/<string:driver_id>/cars/<int:car_id>', methods=['PUT'])
def put_info_car(driver_id, car_id):
    """Modificar el auto de un chofer
    @param car_id es el identificador del auto de un chofer
    @param driver_id es el identificador del chofer"""
    application.logger.info('[PUT] /api/v1/driver/'+str(driver_id)+'/cars/' + str(car_id))
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    if not request.json:
        abort(400)
    response = CLIENT_CONTROLLER.put_new_car(request.json, car_id, driver_id)
    return response

@application.route('/api/v1/driver/<string:driver_id>/cars/<int:car_id>', methods=['DELETE'])
def delete_info_car(driver_id, car_id):
    """Elimina el auto de un chofer
    @param car_id es el identificador del auto de un chofer
    @param driver_id es el identificador del chofer"""
    application.logger.info('[DELETE] /api/v1/driver/'+str(driver_id)+'/cars/' + str(car_id))
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    response = CLIENT_CONTROLLER.delete_car(driver_id, car_id)
    return response

#Endpoints para cobranzas

@application.route('/api/v1/paymentmethods', methods=['GET'])
def get_paymentmethods():
    """Devuelve los metodos de pago que acepta el sistema"""
    application.logger.info('[GET] /api/v1/paymentmethods')
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    response = TRIP_CONTROLLER.get_payment_methods()
    return response

#Endpoints de viajes

@application.route('/api/v1/trips/<int:trip_id>', methods=['GET'])
def get_trip(trip_id):
    """Obtiene la informacion de un viaje
    @param trip_id es el identificador del viaje"""
    application.logger.info('[GET] /trips/' + str(trip_id))
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    response = TRIP_CONTROLLER.get_trip(trip_id)
    return response

#Para pruebas

@swag_from('swagger/helloWord.yml')
@application.route('/')
def hello_word():
    """Devuelve el famoso Hello world"""
    application.logger.info('[TEST] Hello world module - Hello World!')
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    return jsonify(message='hello world')

if __name__ == '__main__':

    if not application.debug and os.environ.get('HEROKU') is None:
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler('access.log', 'a', 1 * 1024 * 1024, 10)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        application.logger.addHandler(file_handler)
        application.logger.setLevel(logging.INFO)
        application.logger.info('Logger startup - NO HEROKU')

    if os.environ.get('HEROKU') is not None:
        import logging
        stream_handler = logging.StreamHandler()
        application.logger.addHandler(stream_handler)
        application.logger.setLevel(logging.INFO)
        application.logger.info('Logger startup')
        application.logger.handlers.extend(logging.getLogger("gunicorn.error").handlers)

    application.run(host='0.0.0.0')
