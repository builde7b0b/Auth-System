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

The /api/register route handles user registration. It checks if the user already exists, hashes the password, and creates a new user in the database.

The /api/login route handles user login. It finds the user by email, compares the provided password with the hashed password, and generates a JWT token if the credentials are valid.

The LoginForm and RegisterForm components from the React side should match these API endpoints.

For example, the loginUser and registerUser functions in the api.js file should make requests to the /api/login and /api/register endpoints, respectively.
