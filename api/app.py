#!flask/bin/python
""" @package api.app
"""
from flask import Flask, jsonify, abort, make_response, request
from api.client_controller import ClientController

app = Flask(__name__)
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

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

#Endpoints de clientes

@app.route('/api/v1/clientedefault', methods=['GET'])
def client_default():
    """Devuelve un ejemplo de la informacion que se debe enviar de un cliente"""
    response = CLIENT_CONTROLLER.get_info_new_client()
    response.status_code = 200
    return response

@app.route('/api/v1/client/<int:client_id>', methods=['GET'])
def get_info_client(client_id):
    """Devuelve la informacion de un cliente"""
    response = CLIENT_CONTROLLER.get_client(client_id)
    response.status_code = 200
    return response

@app.route('/api/v1/client', methods=['POST'])
def post_info_client():
    """Crea un nuevo cliente"""
    if not request.json:
        abort(400)
    response = CLIENT_CONTROLLER.post_new_client(request.json)
    return response

@app.route('/api/v1/client/<int:client_id>', methods=['DELETE'])
def delete_info_client(client_id):
    """Devuelve la informacion de un cliente"""
    response = CLIENT_CONTROLLER.delete_client(client_id)
    return response

@app.route('/')
def hello_word():
    """Devuelve el famoso Hello world"""
    return jsonify(message='hello world')

if __name__ == '__main__':
    app.run(debug=True)
