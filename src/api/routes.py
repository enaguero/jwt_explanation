"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, current_user

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

@api.route('/sign_in', methods=['POST'])
def create_token():
    # We get the params from the request object
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # We look up for the user
    user = User.query.filter_by(email=email).one_or_none()

    # We check if the given password in the params is equal to one created during sign up
    if not user or not user.check_password(password):
        return jsonify("Wrong username or password"), 401
    
    access_token = create_access_token(identity=user)

    return jsonify(access_token=access_token)


@api.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Fetch user profile for the logged-in user."""
    if not current_user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(current_user.serialize()), 200  # ✅ current_user should now be set correctly