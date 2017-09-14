""" @package main
"""
from flask import Flask, jsonify, abort, make_response, request
from flasgger import Swagger
from flasgger.utils import swag_from
from api.client_controller import ClientController
from api.client_controller import TIPO_CLIENTE

#Para levantar swagger hay que ir a http://localhost:5000/apidocs/

application = Flask(__name__)
CLIENT_CONTROLLER = ClientController()

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

@application.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@application.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@application.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

#Endpoints de clientes

@application.route('/api/v1/clientedefault', methods=['GET'])
def client_default():
    """Devuelve un ejemplo de la informacion que se debe enviar de un cliente"""
    response = CLIENT_CONTROLLER.get_info_new_client(TIPO_CLIENTE)
    response.status_code = 200
    return response

@application.route('/api/v1/client/<int:client_id>', methods=['GET'])
def get_info_client(client_id):
    """Devuelve la informacion de un cliente
    @param client_id es el identificador del cliente"""
    response = CLIENT_CONTROLLER.get_client(client_id)
    return response

@application.route('/api/v1/clients', methods=['GET'])
def get_info_clients():
    """Devuelve la informacion de todos los clientes"""
    response = CLIENT_CONTROLLER.get_clients(TIPO_CLIENTE)
    return response

@application.route('/api/v1/client', methods=['POST'])
def post_info_client():
    """Crea un nuevo cliente"""
    if not request.json:
        abort(400)
    response = CLIENT_CONTROLLER.post_new_client(request.json, TIPO_CLIENTE)
    return response

@application.route('/api/v1/client/<int:client_id>', methods=['PUT'])
def put_info_client(client_id):
    """Modificar un cliente
    @param client_id es el identificador del cliente"""
    if not request.json:
        abort(400)
    response = CLIENT_CONTROLLER.put_new_client(request.json, TIPO_CLIENTE, client_id)
    return response

@application.route('/api/v1/client/<int:client_id>', methods=['DELETE'])
def delete_info_client(client_id):
    """Devuelve la informacion de un cliente
    @param client_id es el identificador del cliente"""
    response = CLIENT_CONTROLLER.delete_client(client_id)
    return response

@swag_from('swagger/helloWord.yml')
@application.route('/')
def hello_word():
    """
    Devuelve el famoso Hello world
    """
    return jsonify(message='hello world')

if __name__ == '__main__':
    application.run(host='0.0.0.0')
