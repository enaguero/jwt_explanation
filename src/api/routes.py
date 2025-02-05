"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/sign_up', methods=['POST'])
def sign_up():
    # Type of params: https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request 
    # Security : https://dev.to/goke/securing-your-flask-application-hashing-passwords-tutorial-2f0p

    processed_params = request.get_json()
    print("PARAMS", processed_params)
    new_user = User(email=processed_params['email'], is_active=True)
    new_user.set_password(processed_params['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User was created"}), 201
