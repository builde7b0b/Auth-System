# Auth-System
Authentication System with React Front-end and Flask Backend

# REACT UI SETUP STEPS
1. clone this repo into new directory - git clone 
2. Copy File > api.js from Reusabe repo into new project where we want to integrate login
3. Create new folder > auth in your project 
- Place ReactJS Files into it from Reusable repo.
Add Context File for useAuth Context
4. Add New Components to Routes > App.js
Don't forget to Wrap Entire App in AuthProvider. (App.js)
- Fix issues with Imports / Locations if any
5. Install Dependencies: npm install yup sweetalert2 axios 
6. Check api.js, uncomment unneed functions/methods
- Front-End Should be Displaying after refreshing application. 


# BACKEND - PYTHON/FASK STEPS: 
## Copy Files 
login.py 
app.py
user_model.py

## DB Setup
alternative: use json-server to simulate database interactions 

`npm install -g json-server` 

Create db.json file in root directory
- add sample user data
- Update your backend code (e.g., login.js) to use the json-server endpoints for now:


## Env Setup

To start the Python/Flask backend, follow these steps:

1. Create a virtual environment:
On Windows: python -m venv venv
On macOS/Linux: python3 -m venv venv

2. Activate the virtual environment:
On Windows: venv\Scripts\activate
On macOS/Linux: source venv/bin/activate

3. Install the required packages:
`pip install -r requirements.txt`

4. Start the json-server:
`json-server --watch db.json`
This will start the json-server on http://localhost:3000 and provide the necessary endpoints for your Flask application.

5. Start the Flask application:
`python app.py`
This will start the Flask application on http://localhost:5000.

Now, your Flask backend is up and running, and it's using the json-server to simulate the database interactions for testing purposes.
Make sure that your React application is configured to use the correct API endpoints (e.g., http://localhost:5000/api/auth/register, http://localhost:5000/api/auth/login) to interact with the Flask backend



## Extras & Troubleshooting
### Handle CORS 
### JWT Secret Key Gen

### Login and Auth

These LoginForm.js and RegisterForm.js components should match the API endpoints provided in the api.js file.

The loginUser and registerUser functions in api.js should match the corresponding API endpoints in the backend (Flask or Node.js/Express).

For example, in the api.js file, the loginUser and registerUser functions should make the appropriate requests to the /login and /register endpoints, respectively, on the backend.

### Express / Node

This example uses Express.js for the backend and Mongoose for the User model. The server.js file defines two routes: /api/register and /api/login.

## Stripe Integration

This project includes a complete Stripe payment processing system that allows users to upgrade to premium status. The integration uses Stripe's PaymentIntent API for secure payment processing.

### Features

- Secure payment processing with Stripe Elements
- Premium subscription management
- User subscription status tracking
- Environment-specific configuration (test/production)

### Frontend Implementation

The frontend uses the official Stripe React libraries:

The /api/register route handles user registration. It checks if the user already exists, hashes the password, and creates a new user in the database.

The /api/login route handles user login. It finds the user by email, compares the provided password with the hashed password, and generates a JWT token if the credentials are valid.

The LoginForm and RegisterForm components from the React side should match these API endpoints.

For example, the loginUser and registerUser functions in the api.js file should make requests to the /api/login and /api/register endpoints, respectively.
```
// Stripe Elements setup in index.js
import { Elements } from '@stripe/react-stripe-js';
import { loadStripe } from '@stripe/stripe-js';
// For development (test mode)
const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_KEY);
// For production
// const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_KEY_PROD);
// Wrap your app with the Stripe Elements provider
root.render(
<React.StrictMode>
<Elements stripe={stripePromise}>
<App />
</Elements>
</React.StrictMode>
);

```
### Backend Implementation

The backend handles payment intents creation and subscription status management:
Create a payment intent
```
@bp.route('/api/create-payment-intent', methods=['POST'])
def create_payment_intent():
try:
data = request.json
intent = stripe.PaymentIntent.create(
amount=data['amount'], # amount in cents
currency='usd',
)
return jsonify({
'clientSecret': intent['client_secret'],
'id': intent['id']
})
except Exception as e:
return jsonify(error=str(e)), 400
```
Check user's subscription status
```
@bp.route('/check-subscription', methods=['GET'])
@jwt_required()
def check_subscription_status():
mongo = app.config['MONGO_INSTANCE']
current_user_email = get_jwt_identity()
user = mongo.db.users.find_one({'email': current_user_email})
if user and 'is_premium' in user:
return jsonify({'isPremium': user['is_premium']}), 200
else:
return jsonify({'error': 'User not found or subscription status unavailable'}), 404
```
Update user to premium status after successful payment
```
@bp.route('/update-premium-status', methods=['POST'])
@jwt_required()
def update_premium_status():
mongo = app.config['MONGO_INSTANCE']
current_user_email = get_jwt_identity()
user = mongo.db.users.find_one({'email': current_user_email})
if not user:
return jsonify({'error': 'User not found'}), 404
update_result = mongo.db.users.update_one(
{'id': ObjectId(user['_id'])},
{'$set': {'is_premium': True}}
)
return jsonify({'result': 'User status updated to premium'}), 200
```

### Environment Configuration

The integration supports both test and production environments:

#### Backend
TESTING
`stripe.api_key = os.environ.get('STRIPE_API_SECRET_TEST')`
PRODUCTION
`stripe.api_key = os.environ.get('STRIPE_API_SECRET_PROD')`

#### Frontend
```
// const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_KEY_PROD);
```


### Implementation Steps

1. **Set up environment variables**:
   - `REACT_APP_STRIPE_KEY`: Your Stripe publishable key for test mode
   - `REACT_APP_STRIPE_KEY_PROD`: Your Stripe publishable key for production
   - `STRIPE_API_SECRET_TEST`: Your Stripe secret key for test mode
   - `STRIPE_API_SECRET_PROD`: Your Stripe secret key for production

2. **Create a payment form component** that uses Stripe Elements to collect card information securely.

3. **Implement the payment flow**:
   - Frontend sends a request to create a payment intent
   - Backend creates the payment intent and returns the client secret
   - Frontend uses the client secret to confirm the payment with Stripe.js
   - On successful payment, backend updates the user's premium status

4. **Add subscription status checking** to enable/disable premium features based on the user's status.

### Testing

For testing, use Stripe's test cards:

- Success: `4242 4242 4242 4242`
- Requires Authentication: `4000 0025 0000 3155`
- Declined: `4000 0000 0000 0002`

Use any future expiration date, any 3-digit CVC, and any postal code.

### Going to Production

When ready to go live:

1. Uncomment the production Stripe key lines in both frontend and backend
2. Comment out the test key lines
3. Ensure your Stripe account is properly configured for live payments
4. Test the entire payment flow in production mode with real cards
