import os
import json
import jwt
import datetime
from flask import session, jsonify, request, Blueprint, current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

bp = Blueprint('login', __name__)
jwt = JWTManager(app)

# Path to the JSON file
JSON_FILE = 'db.json'

def get_users_from_json():
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    return data.get('users', [])

def get_user_by_email(email):
    users = get_users_from_json()
    return next((user for user in users if user['email'] == email), None)

def create_user(email, hashed_password):
    users = get_users_from_json()
    new_user = {
        'id': len(users) + 1,
        'email': email,
        'hashed_password': hashed_password,
        'created_at': datetime.datetime.utcnow().isoformat(),
        'updated_at': datetime.datetime.utcnow().isoformat(),
        'is_premium': False
    }
    users.append(new_user)
    with open(JSON_FILE, 'w') as f:
        json.dump({'users': users}, f)
    return new_user

@bp.route('/register', methods=['POST'])
def register():
    email = request.json['email']
    password = request.json['password']

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    if get_user_by_email(email):
        return jsonify({'error': 'User with this email already exists'}), 409

    hashed_password = generate_password_hash(password)
    user = create_user(email, hashed_password)
    return jsonify({'result': 'User registered'})

@bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user = get_user_by_email(email)

    if not user or not check_password_hash(user['hashed_password'], password):
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=user['email'])
    return jsonify({
        'token': access_token,
        'isPremium': user.get('is_premium', False)
    }), 200

@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Add token to a blacklist
    return jsonify({'result': 'Logged out'})

@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200