#USER REGISTRATION AND AUTHENTICATION 
from flask import session, jsonify, request, Blueprint, current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt 
import datetime 
from flask_jwt_extended import JWTManager, create_access_token


SECRET_KEY = "your-secret-key" #, this should be in our config file, config.py



bp = Blueprint('login', __name__)
@bp.route('/register', methods=['POST'])
def register():
    mongo = app.config['MONGO_INSTANCE']
    
    users = mongo.db.users 
    email = request.json['email']
    password = request.json['password']


    #Add validation and password hasing here 
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    # Check for existing user with the same email
    existing_user = users.find_one({'email': email})
    if existing_user:
        return jsonify({'error': 'User with this email already exists'}), 409
    
    hashed_password = generate_password_hash(password)
    users.insert_one({
        'email': email, 
        'hashed_password': hashed_password,
        'is_premium': False,
        'created_at': datetime.datetime.utcnow(),
        'updated_at': datetime.datetime.utcnow()
        })
    return jsonify({'result': 'User registered'})
    


@bp.route('/login', methods=['POST'])
def login():
    mongo = app.config['MONGO_INSTANCE']
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    users = mongo.db.users 
    user = users.find_one({'email': email})

    if not user or not check_password_hash(user['hashed_password'], password):
        return jsonify({"msg": "Bad username or password"}), 401

    # Generate the token
    access_token = create_access_token(identity=user['email'])
    # return jsonify(token=access_token), 200
    return jsonify({
        'token': access_token,
        'isPremium': user.get('is_premium', False)
    }), 200


    # app.secret_key = 'your-secret-key'
    # mongo = app.config['MONGO_INSTANCE']
    # users = mongo.db.users 
    # email = request.json.get('email')
    # password = request.json.get('password')

    # user = users.find_one({'email': email})

    # if not user or not check_password_hash(user['hashed_password'], password):
    #     return jsonify({'error': 'Invalid email or password'}), 401
    
    # # Set the authenticated_user_email in the user's session or as a cookie
    # session['authenticated_user_email'] = email

    #  # Print session data for debugging
    # print('Session Data:', session)
    
    # # Generate a token and return it (We'll implement this next)
    # token = jwt.encode({
    #     'user_id': str(user['_id']),
    #     'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    # }, SECRET_KEY, algorithm='HS256')

    # return jsonify({'token': token})



@bp.route('/logout', methods=['POST'])
def logout():
    token = request.json.get('token')
    # Add token to a blacklist 
    return jsonify({'result': 'Logged out'})