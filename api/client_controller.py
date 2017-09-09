#!flask/bin/python
from flask import Flask, jsonify, abort, make_response
from model.client_shared import ClientShared

app = Flask(__name__)

@app.route('/uberfiuba/v1/clientedefault', methods=['GET'])
def get_info_new_client():
    client = ClientShared.new_client(1, "cliente", "pepelopez", "password", "fb_user_id", "fb_auth_token", "pepe", "lopez", "Argentina", "pepe@gmail.com", "21/01/2000")
    response = client.get_json_new_client()
    response.status_code = 200
    return response

if __name__ == '__main__':
    app.run(debug=True)