""" @package main
"""
import os
from flask import Flask, jsonify, abort, make_response, request, session
from flasgger import Swagger
from flasgger.utils import swag_from
from api.client_controller import ClientController
from api.trip_controller import TripController
from api.transaction_controller import TransactionController
from api.google_directions_controller import DirectionsController
from service.shared_server import TIPO_CLIENTE
from service.shared_server import TIPO_CHOFER
from service.login_service import LoginService

#Para levantar swagger hay que ir a http://localhost:5000/apidocs/

application = Flask(__name__)

TRANSACTION_CONTROLLER = TransactionController()
TRIP_CONTROLLER = TripController()
CLIENT_CONTROLLER = ClientController()
LOGIN_SERVICE = LoginService()
GOOGLE_SERVICE = DirectionsController()

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
    @param password es la contrasenia del usuario"""
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

@application.route('/api/v1/closestdrivers/latitude/<string:lat>/length/<string:lon>/radio/<string:radio>', methods=['GET'])
def get_info_closest_drivers(lat, lon, radio):
    """Devuelve la informacion de todos los choferes cercanos
        @param lat es la latitud del lugar donde se busca a los choferes
        @param lon es la longitud del lugar donde se busca a los choferes
        @param radio es el radio donde se va a buscar a los choferes"""
    application.logger.info('[GET] /api/v1/closestdrivers')
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    _lat = float(lat)
    _lon = float(lon)
    _radio = float(radio)
    response = CLIENT_CONTROLLER.get_closest_clients(TIPO_CHOFER, _lat, _lon, _radio)
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
    response = TRANSACTION_CONTROLLER.get_payment_methods()
    return response

@application.route('/api/v1/driver/<string:driver_id>/transactions', methods=['GET'])
def get_transactions_driver(driver_id):
    """Devuelve los metodos de pago que acepta el sistema"""
    application.logger.info('[GET] /api/v1/driver/' + str(driver_id) + '/transactions')
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    response = TRANSACTION_CONTROLLER.get_transactions(driver_id)
    return response

@application.route('/api/v1/client/<string:client_id>/transactions', methods=['GET'])
def get_transactions_client(client_id):
    """Devuelve los metodos de pago que acepta el sistema"""
    application.logger.info('[GET] /api/v1/client/' + str(client_id) + '/transactions')
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    response = TRANSACTION_CONTROLLER.get_transactions(client_id)
    return response

@application.route('/api/v1/driver/<string:driver_id>/transactions', methods=['POST'])
def post_info_transaction_driver(driver_id):
    """Guarda la informacion de la transaccion del chofer
    @param driver_id es el identificador del chofer"""
    application.logger.info('[POST] /api/v1/driver/'+str(driver_id)+'/transactions')
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    if not request.json:
        abort(400)
    response = TRANSACTION_CONTROLLER.post_transactions(request.json, driver_id)
    return response

@application.route('/api/v1/client/<string:client_id>/transactions', methods=['POST'])
def post_info_transaction_client(client_id):
    """Guarda la informacion de la transaccion del cliente
    @param client_id es el identificador del cliente"""
    application.logger.info('[POST] /api/v1/client/'+str(client_id)+'/transactions')
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    if not request.json:
        abort(400)
    response = TRANSACTION_CONTROLLER.post_transactions(request.json, client_id)
    return response

#Endpoints de viajes

@application.route('/api/v1/driver/<string:driver_id>/trips/<int:trip_id>', methods=['GET'])
def get_trip_driver(driver_id, trip_id):
    """Obtiene la informacion del viaje de un chofer
    @param driver_id es el identificador del chofer
    @param trip_id es el identificador del viaje"""
    application.logger.info('[GET] /api/v1/driver/' + str(driver_id) + '/trips/' + str(trip_id))
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    response = TRIP_CONTROLLER.get_trip(TIPO_CHOFER, driver_id, trip_id)
    return response

@application.route('/api/v1/client/<string:client_id>/trips/<int:trip_id>', methods=['GET'])
def get_trip_client(client_id, trip_id):
    """Obtiene la informacion del viaje de un cliente
    @param client_id es el identificador del cliente
    @param trip_id es el identificador del viaje"""
    application.logger.info('[GET] /api/v1/client/' + str(client_id) + '/trips/' + str(trip_id))
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    response = TRIP_CONTROLLER.get_trip(TIPO_CLIENTE, client_id, trip_id)
    return response

@application.route('/api/v1/driver/<string:driver_id>/trips', methods=['GET'])
def get_trips_driver(driver_id):
    """Obtiene la informacion del viaje de un chofer
    @param driver_id es el identificador del chofer
    @param trip_id es el identificador del viaje"""
    application.logger.info('[GET] /api/v1/driver/' + str(driver_id) + '/trips')
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    response = TRIP_CONTROLLER.get_trips(driver_id)
    return response

@application.route('/api/v1/client/<string:client_id>/trips', methods=['GET'])
def get_trips_client(client_id):
    """Obtiene la informacion de los viajes de un cliente
    @param client_id es el identificador del cliente"""
    application.logger.info('[GET] /api/v1/client/' + str(client_id) + '/trips')
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    response = TRIP_CONTROLLER.get_trips(client_id)
    return response

@application.route('/api/v1/driver/<string:driver_id>/trips/<string:trip_id>/accept', methods=['PUT'])
def get_trips_driver_accept(driver_id, trip_id):
    """El chofer acepta realizar un viaje
    @param driver_id es el identificador del chofer
    @param trip_id es el identificador del viaje"""
    application.logger.info('[PUT] /api/v1/driver/' + str(driver_id) + '/trips/'
                            + str(trip_id) + '/accept')
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    response = TRIP_CONTROLLER.accept_trip(driver_id, trip_id)
    return response

@application.route('/api/v1/client/<string:client_id>/trips/<string:trip_id>/start', methods=['PUT'])
def get_trips_client_start(client_id, trip_id):
    """El cliente confirma que comenzo el viaje
    @param client_id es el identificador del cliente
    @param trip_id es el identificador del viaje"""
    application.logger.info('[PUT] /api/v1/driver/' + str(client_id) + '/trips/'
                            + str(trip_id) + '/start')
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    response = TRIP_CONTROLLER.start_trip(client_id, trip_id)
    return response

@application.route('/api/v1/client/<string:client_id>/trips/<string:trip_id>/finish', methods=['PUT'])
def get_trips_client_finish(client_id, trip_id):
    """El cliente confirma que termino el viaje
    @param client_id es el identificador del cliente
    @param trip_id es el identificador del viaje"""
    application.logger.info('[PUT] /api/v1/client/' + str(client_id) + '/trips/'
                            + str(trip_id) + '/finish')
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    response = TRIP_CONTROLLER.finish_trip(client_id, trip_id)
    return response

@application.route('/api/v1/trips/estimate', methods=['POST'])
def post_estimate():
    """Devuelve la estimacion de un viaje
    """
    application.logger.info('[POST] /api/v1/trips/estimate')
    #Veo si esta logueado
    if not is_logged():
        return response_invalid_login()
    if not request.json:
        abort(400)
    response = TRIP_CONTROLLER.post_new_estimate(request.json)
    return response

@application.route('/api/v1/client/<string:client_id>/trips', methods=['POST'])
def post_trip(client_id):
    """Crea un viaje"""
    application.logger.info('[POST] /api/v1/trip')
    #check de login
    if not is_logged():
        return response_invalid_login()
    if not request.json:
        abort(400)
    response = TRIP_CONTROLLER.post_new_trip(request.json)
    return response

@application.route('/api/v1/availabletrips/<string:user_id>', methods=['GET'])
def get_available_trips(user_id):
    """Obtiene los viajes disponibles dado un id de un driver"""
    application.logger.info('[GET] /api/v1/availabletrips with user_id: ' + str(user_id))
    #check de login
    if not is_logged():
        return response_invalid_login()
    response = TRIP_CONTROLLER.get_available_trips(user_id)
    return response

@application.route('/api/v1/client/<string:client_id>/newtrips', methods=['GET'])
def get_new_trips_by_client(client_id):
    """Devuelve los viajes pedidos un cliente"""
    #check de login
    if not is_logged():
        return response_invalid_login()
    response = TRIP_CONTROLLER.get_trips_by_client(client_id)
    return response

@application.route('/api/v1/driver/<string:driver_id>/newtrips', methods=['GET'])
def get_new_trips_by_driver(driver_id):
    """Devuelve los viajes pedidos de un driver"""
    #check de login
    if not is_logged():
        return response_invalid_login()
    response = TRIP_CONTROLLER.get_trips_by_driver(driver_id)
    return response

# @application.route('/api/v1/ongoingtrips', methods=['GET'])
# def get_ongoing_trips():
#     """Devuelve los viajes que no finalizaron (sin stamp de trip end)"""

#     response = TRIP_CONTROLLER.get_ongoing_trips()
#     return response

#Endpoints de Google API
@application.route('/api/v1/trajectories', methods=['POST'])
def get_directions():
    """Devuelve las posibles rutas de un punto a otro"""
    application.logger.info('[POST] /api/v1/trajectories')
    #check de login
    if not is_logged():
        return response_invalid_login()
    if not request.json:
        abort(400)
    response = GOOGLE_SERVICE.get_google_directions(request.json)
    return response

#Endpoints test de mongo!
@application.route('/api/v1/lastlocation/<string:client_id>', methods=['GET'])
def get_last_location(client_id):
    """Devuelve la ultima ubicacion conocida de un usuario
    """
    application.logger.info('[GET] /api/v1/lastlocation')
    if not is_logged():
        return response_invalid_login()
    response = TRIP_CONTROLLER.get_last_location(client_id)
    return response

@application.route('/api/v1/lastlocation', methods=['POST'])
def add_last_location():
    """ Agrega la ultima ubicacion asociada a un usuario
    """
    application.logger.info('[POST] /api/v1/lastlocation')
    if not is_logged():
        return response_invalid_login()
    if not request.json:
        abort(400)
    response = TRIP_CONTROLLER.post_new_last_location(request.json)
    return response

# @application.route('/api/v1/mongoclient', methods=['POST'])
# def add_mongo_user():
#     """ Agrega un nuevo usuario a mongo"""
#     application.logger.info('[POST] /api/v1/mongoclient')
#     if not is_logged():
#         return response_invalid_login()
#     if not request.json:
#         abort(400)
#     response = TRIP_CONTROLLER.post_new_app_user(request.json)
#     return response

# @application.route('/api/v1/mongoclients', methods=['GET'])
# def get_mongo_users():
#     """ Obtiene los usuarios de mongo"""
#     application.logger.info('[GET] /api/v1/mongoclients')
#     if not is_logged():
#         return response_invalid_login()
#     response = TRIP_CONTROLLER.get_mongo_users()
#     return response

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
