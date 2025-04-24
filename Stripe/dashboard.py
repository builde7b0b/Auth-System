import os
from flask import Blueprint, jsonify, request, current_app as app, Response
import csv
import stripe 
from dotenv import load_dotenv
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId 


load_dotenv()
# stripe.api_key = ''  # Set your Stripe secret key

# TESTING
stripe.api_key = os.environ.get('STRIPE_API_SECRET_TEST')

# PRODUCTION
# stripe.api_key = os.environ.get('STRIPE_API_SECRET_PROD')

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard', methods=['GET'])
def dashboard():
    mongo = app.config['MONGO_INSTANCE']
    collections = mongo.db.collections 
    collection_id = request.args.get('collection_id')
    collection = collections.find_one({'_id': collection_id})
    # returns null if nothing if no data is found 
    # we must use 
    return jsonify(collection)


@bp.route('/email_list', methods=['GET'])
def email_list():
    mongo = app.config['MONGO_INSTANCE']
    emails = mongo.db.emails 
    collection_id = request.args.get('collection_id') 

    # Fetch emails related to this collection 
    email_list = emails.find({'collection_id': collection_id})
    return jsonify(list(email_list))


    # dashsboard logic here

# TODO: Add features, pagination, sorting, and filtering to make the dashboard more user-friendly, TEST ENDPOINTS, Make sure to pass in a valid collection_id in the request URL as a query parameter.

@bp.route('/export_csv', methods=['GET'])
def export_csv():
    # export logic here
    mongo = app.config['MONGO_INSTANCE']
    emails = mongo.db.emails 
    collection_id = request.args.get('collection_id')

    email_list = emails.find({'collection_id': collection_id})

    def generate():
        yield ','.join(["email", "user_id"]) + '\n'
        for email in email_list:
            yield f"{email['email']},{email['user_id']}\n"

    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment; filename=email_list.csv"})



@bp.route('/api/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        data = request.json
        intent = stripe.PaymentIntent.create(
            amount=data['amount'],  # amount in cents
            currency='usd',
        )
        return jsonify({
            'clientSecret': intent['client_secret'],
            'id': intent['id']
        })
    except Exception as e:
        return jsonify(error=str(e)), 400
    


@bp.route('/check-subscription', methods=['GET'])
@jwt_required()
def check_subscription_status():
    mongo = app.config['MONGO_INSTANCE']

    current_user_email = get_jwt_identity()

    # Query your database to check the user's subscription status
    # This is a placeholder logic, adjust according to your database schema
    user = mongo.db.users.find_one({'email': current_user_email})
    if user and 'is_premium' in user:
        return jsonify({'isPremium': user['is_premium']}), 200
    else:
        return jsonify({'error': 'User not found or subscription status unavailable'}), 404

# ... rest of your Flask app ...

@bp.route('/update-premium-status', methods=['POST'])
@jwt_required()
def update_premium_status():
    mongo = app.config['MONGO_INSTANCE']
    current_user_email = get_jwt_identity()
    print(request.headers)

    # Find the user by their email
    user = mongo.db.users.find_one({'email': current_user_email})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    print(user)

    # Update the user's is_premium status
    update_result = mongo.db.users.update_one(
        {'_id': ObjectId(user['_id'])},
        {'$set': {'is_premium': True}}
    )

    print("Update operation result:", update_result.raw_result)

    return jsonify({'result': 'User status updated to premium'}), 200



