""" @package main
"""
import os
from flask import Flask, jsonify, abort, make_response, request
from api.client_controller import ClientController
from api.client_controller import TIPO_CLIENTE

application = Flask(__name__)
CLIENT_CONTROLLER = ClientController()

tasks = [
    {
        'id': 1,
        'title': u'Aprender Docker',
        'description': u'todo el dia perdido en intentar hacerlo andar',
        'done': False
    },
    {
        'id': 2,
        'title': u'Aprender Flask',
        'description': u'Por suerte no es tan complicado',
        'done': False
    }
]

@application.route('/todo/api/v1/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@application.route('/todo/api/v1/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@application.errorhandler(404)
def not_found(error):
    """Manejador de error para codigo 404"""
    application.logger.error('Error 404 - Recurso no encontrado')
    return make_response(jsonify({'error': 'Not Found'}), 404)

@application.route('/logtest')
def logTest():
    application.logger.warning('Testeando Warning!')
    application.logger.error('Testeando Error!')
    application.logger.info('Testeando Info!')
    return "Testeando el Logger..."

#Endpoints de clientes

@application.route('/api/v1/clientedefault', methods=['GET'])
def client_default():
    """Devuelve un ejemplo de la informacion que se debe enviar de un cliente"""
    application.logger.info('[GET] /api/v1/clientedefault')
    response = CLIENT_CONTROLLER.get_info_new_client(TIPO_CLIENTE)
    response.status_code = 200
    return response

@application.route('/api/v1/client/<int:client_id>', methods=['GET'])
def get_info_client(client_id):
    """Devuelve la informacion de un cliente
    @param client_id es el identificador del cliente"""
    application.logger.info('[GET] /api/v1/client/' + str(client_id))
    response = CLIENT_CONTROLLER.get_client(client_id)
    return response

@application.route('/api/v1/clients', methods=['GET'])
def get_info_clients():
    """Devuelve la informacion de todos los clientes"""
    application.logger.info('[GET] /api/v1/clients')
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

@application.route('/api/v1/client/<int:client_id>', methods=['PUT'])
def put_info_client(client_id):
    """Modificar un cliente
    @param client_id es el identificador del cliente"""
    application.logger.info('[PUT] /api/v1/client/' + str(client_id))
    if not request.json:
        abort(400)
    response = CLIENT_CONTROLLER.put_new_client(request.json, TIPO_CLIENTE, client_id)
    return response

@application.route('/api/v1/client/<int:client_id>', methods=['DELETE'])
def delete_info_client(client_id):
    """Devuelve la informacion de un cliente
    @param client_id es el identificador del cliente"""
    application.logger.info('[DELETE] /api/v1/client/' + str(client_id))
    response = CLIENT_CONTROLLER.delete_client(client_id)
    return response



@application.route('/')
def hello_word():
    """Devuelve el famoso Hello world"""
    application.logger.info('[TEST] Hello world module - Hello World!')
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