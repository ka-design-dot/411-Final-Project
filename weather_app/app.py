import os
import sqlite3
from flask import Flask, jsonify, request, Response, make_response 
import requests
from utils.logger import configure_logger  # Import the configure_logger from your logger file
from model.user_storage_model import Users, create_user, check_password, delete_user, get_id_by_username, update_password
from werkzeug.exceptions import BadRequest, Unauthorized
from db import db
from dotenv import load_dotenv
# load_dotenv()

# OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

# app = Flask(__name__)

# # Set up the logger using your pre-configured logger
# configure_logger(app.logger)

# # Database configuration
# DATABASE = 'weather_list.db' 

# def get_db():
#     """ Get a connection to the database """
#     conn = sqlite3.connect(DATABASE)
#     return conn

# def init_db():
#     """ Initialize the database by running SQL commands from the user.sql file """
#     with sqlite3.connect(DATABASE) as conn:
#         with open('user.sql', 'r') as sql_file:
#             sql_script = sql_file.read()
#         conn.executescript(sql_script)
#         app.logger.info("Database initialized from user.sql")

# @app.before_request
# def before_first_request():
#     """ Initialize the database the first time the app is run """
#     if not os.path.exists(DATABASE):
#         init_db()
#         app.logger.info(f"Database {DATABASE} created successfully.")
#     else:
#         app.logger.info(f"Database {DATABASE} already exists.")

# @app.route('/api/health', methods=['GET'])
# def healthcheck():
#     """ Health check route to verify the service is running """
#     app.logger.info('Health check')
#     return jsonify({'status': 'healthy'}), 200

#  ##########################################################
# #
# # User management
# #
# ##########################################################

# @app.route('/api/create-user', methods=['POST'])
# def create_user() -> Response:
#     """
#     Route to create a new user.

#     Expected JSON Input:
#             - username (str): The username for the new user.
#             - password (str): The password for the new user.

#     Returns:
#         JSON response indicating the success of user creation.
#     Raises:
#         400 error if input validation fails.
#         500 error if there is an issue adding the user to the database.
#     """
#     app.logger.info('Creating new user')
#     try:
#         # Get the JSON data from the request
#         data = request.get_json()

#         # Extract and validate required fields
#         username = data.get('username')
#         password = data.get('password')

#         if not username or not password:
#             return make_response(jsonify({'error': 'Invalid input, both username and password are required'}), 400)

#         # Call the User function to add the user to the database
#         app.logger.info('Adding user: %s', username)
#         Users.create_user(username, password)

#         app.logger.info("User added: %s", username)
#         return make_response(jsonify({'status': 'user added', 'username': username}), 201)
#     except Exception as e:
#         app.logger.error("Failed to add user: %s", str(e))
#         return make_response(jsonify({'error': str(e)}), 500)

# @app.route('/api/delete-user', methods=['DELETE'])
# def delete_user() -> Response:
#     """
#     Route to delete a user.

#     Expected JSON Input:
#          - username (str): The username of the user to be deleted.

#     Returns:
#         JSON response indicating the success of user deletion.
#     Raises:
#         400 error if input validation fails.
#         500 error if there is an issue deleting the user from the database.
#     """
#     app.logger.info('Deleting user')
#     try:
#         # Get the JSON data from the request
#         data = request.get_json()

#         # Extract and validate required fields
#         username = data.get('username')

#         if not username:
#             return make_response(jsonify({'error': 'Invalid input, username is required'}), 400)

#         # Call the User function to delete the user from the database
#         app.logger.info('Deleting user: %s', username)
#         Users.delete_user(username)

#         app.logger.info("User deleted: %s", username)
#         return make_response(jsonify({'status': 'user deleted', 'username': username}), 200)
#     except Exception as e:
#         app.logger.error("Failed to delete user: %s", str(e))
#         return make_response(jsonify({'error': str(e)}), 500)

# @app.route('/api/login', methods=['POST'])
# def login():
#     """
#     Route to log in a user and load their combatants.

#     Expected JSON Input:
#        - username (str): The username of the user.
#         - password (str): The user's password.

#     Returns:
#          JSON response indicating the success of the login.

#     Raises:
#         400 error if input validation fails.
#         401 error if authentication fails (invalid username or password).
#         500 error for any unexpected server-side issues.
#     """
#     data = request.get_json()
#     if not data or 'username' not in data or 'password' not in data:
#         app.logger.error("Invalid request payload for login.")
#         raise BadRequest("Invalid request payload. 'username' and 'password' are required.")

#     username = data['username']
#     password = data['password']

#     try:
#         # Validate user credentials
#         if not Users.check_password(username, password):
#             app.logger.warning("Login failed for username: %s", username)
#             raise Unauthorized("Invalid username or password.")

#         # Get user ID
#         user_id = Users.get_id_by_username(username)

#         # Load user's combatants into the battle model
#         #login_user(user_id, battle_model)

#         app.logger.info("User %s logged in successfully.", username)
#         return jsonify({"message": f"User {username} logged in successfully."}), 200

#     except Unauthorized as e:
#         return jsonify({"error": str(e)}), 401
#     except Exception as e:
#         app.logger.error("Error during login for username %s: %s", username, str(e))
#         return jsonify({"error": "An unexpected error occurred."}), 500


######################################################################################################

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)
# CORS(app)  # Enable Cross-Origin Resource Sharing
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DATABASE = 'weather_list.db'
API_KEY = os.getenv('OPENWEATHER_API_KEY')

# Rate Limiting
# limiter = Limiter(app)


# Logger configuration
def configure_logger(logger):
    import logging
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
    logger.addHandler(handler)


configure_logger(app.logger)


# Database Initialization
def init_db():
    """Initialize the database."""
    with sqlite3.connect(DATABASE) as conn:
        with open('user.sql', 'r') as sql_file:
            sql_script = sql_file.read()
        conn.executescript(sql_script)
        app.logger.info("Database initialized from user.sql")


@app.before_request
def before_first_request():
    """Ensure database exists before handling requests."""
    if not os.path.exists(DATABASE):
        init_db()
        app.logger.info(f"Database {DATABASE} created successfully.")
    else:
        app.logger.info(f"Database {DATABASE} already exists.")


# User Management Routes
@app.route('/api/create-user', methods=['POST'])
def create_user() -> Response:
    """
    Create a new user.
    """
    app.logger.info('Creating new user')
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise BadRequest("Both username and password are required.")

        with sqlite3.connect(DATABASE) as conn:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

        app.logger.info(f"User {username} created successfully.")
        return jsonify({'status': 'user created', 'username': username}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400
    except Exception as e:
        app.logger.error(f"Error creating user: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/delete-user', methods=['DELETE'])
def delete_user() -> Response:
    """
    Delete a user.
    """
    app.logger.info('Deleting user')
    try:
        data = request.get_json()
        username = data.get('username')

        if not username:
            raise BadRequest("Username is required.")

        with sqlite3.connect(DATABASE) as conn:
            conn.execute("DELETE FROM users WHERE username = ?", (username,))

        app.logger.info(f"User {username} deleted successfully.")
        return jsonify({'status': 'user deleted', 'username': username}), 200
    except Exception as e:
        app.logger.error(f"Error deleting user: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/login', methods=['POST'])
# @limiter.limit("10 per minute")
def login():
    """
    Login a user.
    """
    app.logger.info('User login')
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise BadRequest("Both username and password are required.")

        with sqlite3.connect(DATABASE) as conn:
            user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if not user or user[2] != password:  # Assuming password is in the 3rd column
            raise Unauthorized("Invalid username or password.")

        app.logger.info(f"User {username} logged in successfully.")
        return jsonify({'status': 'login successful', 'username': username}), 200
    except Unauthorized as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        app.logger.error(f"Error logging in: {e}")
        return jsonify({'error': str(e)}), 500


# Weather Routes
@app.route('/api/weather/<location>', methods=['GET'])
def get_weather(location):
    """
    Fetch current weather for a location.
    """
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        return jsonify({
            'location': location,
            'temperature': weather_data['main']['temp'],
            'humidity': weather_data['main']['humidity'],
            'wind_speed': weather_data['wind']['speed'],
            'description': weather_data['weather'][0]['description']
        })
    except requests.RequestException as e:
        app.logger.error(f"Error fetching weather: {e}")
        return jsonify({'error': 'Failed to fetch weather data'}), 500


@app.route('/api/forecast/<location>', methods=['GET'])
def get_forecast(location):
    """
    Fetch weather forecast for a location.
    """
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        forecast_data = response.json()
        forecasts = [
            {'date': item['dt_txt'], 'temperature': item['main']['temp'], 'description': item['weather'][0]['description']}
            for item in forecast_data['list']
        ]
        return jsonify(forecasts)
    except requests.RequestException as e:
        app.logger.error(f"Error fetching forecast: {e}")
        return jsonify({'error': 'Failed to fetch forecast data'}), 500


# Health Check
@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check route to verify the service is running.
    """
    try:
        sqlite3.connect(DATABASE).close()
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        app.logger.error(f"Health check failed: {e}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500


# Main
if __name__ == '__main__':
    app.run(debug=True)

