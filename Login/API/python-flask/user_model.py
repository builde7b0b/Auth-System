from flask import current_app as app 
from werkzeug.security import generate_password_hash
import datetime 

def create_user(email, password):
    mongo = app.config['MONGO_INSTANCE']
    hashed_password = generate_password_hash(password)
    user = {
        'email': email,
        'hashed_password': hashed_password,
        'created_at': datetime.datetime.utcnow(),
        'updated_at': datetime.datetime.utcnow(),
        'is_premium': False
    }
    mongo.db.users.insert_one(user)
    return user 

## Add more functions