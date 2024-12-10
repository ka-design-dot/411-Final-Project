
from flask import Flask, request, jsonify
from flask import Response, make_response
from weather_app.models.favorite_list_model import FavoriteListModel
from weather_app.utils.sql_utils import check_database_connection, check_table_exists
from weather_app.models.user_model import UserModel

app = Flask(__name__)
favorites_model = FavoriteListModel()
user_model = UserModel()
API_KEY =  "your_openweathermap_api_key"  # Replace with your actual API key

###################################################################################################################


###############################################################
# HEALTHCHECKS
###############################################################

@app.route('/api/health', methods=['GET'])
def healthcheck() -> Response:
    """
    Health check route to verify the service is running.

    Returns:
        JSON response indicating the health status of the service.
    """
    app.logger.info('Health check')
    return make_response(jsonify({'status': 'healthy'}), 200)

@app.route('/api/db-check', methods=['GET'])
def db_check() -> Response:
    """
    Route to check if the database connection and meals table are functional.

    Returns:
        JSON response indicating the database health status.
    Raises:
        404 error if there is an issue with the database.
    """
    try:
        app.logger.info("Checking database connection...")
        check_database_connection()
        app.logger.info("Database connection is OK.")
        app.logger.info("Checking if meals table exists...")
        check_table_exists("meals")
        app.logger.info("meals table exists.")
        return make_response(jsonify({'database_status': 'healthy'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 404)


####################################################################################################################


###############################################################
# USERS
###############################################################

@app.route('/auth/create-account', methods=['POST'])
def create_account():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        user_model.create_account(username, password)
        return jsonify({"message": "Account created successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if user_model.login(username, password):
        # Generate and return a session token (implement token generation if needed)
        return jsonify({"message": "Login successful", "token": "fake-token-for-now"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/auth/update-password', methods=['PUT'])
def update_password():
    data = request.json
    username = data.get('username')
    new_password = data.get('new_password')

    if not username or not new_password:
        return jsonify({"error": "Username and new password are required"}), 400

    try:
        user_model.update_password(username, new_password)
        return jsonify({"message": "Password updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
####################################################################################################################

###############################################################
# FAVORITE LIST MODEL 
###############################################################

@app.route('/favorites/add', methods=['POST'])
def add_city():
    """Add a city to the user's favorites."""
    data = request.json
    user_id = data.get('user_id')
    city_name = data.get('city_name')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not all([user_id, city_name, latitude, longitude]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        favorites_model.add_city(user_id, city_name, latitude, longitude)
        return jsonify({"message": f"City {city_name} added to favorites"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/favorites/remove', methods=['DELETE'])
def remove_city():
    """Remove a city from the user's favorites."""
    data = request.json
    user_id = data.get('user_id')
    city_name = data.get('city_name')

    if not all([user_id, city_name]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        favorites_model.remove_city(user_id, city_name)
        return jsonify({"message": f"City {city_name} removed from favorites"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/favorites', methods=['GET'])
def get_all_favorites():
    """Retrieve all favorite cities for a user."""
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "Missing required field: user_id"}), 400

    try:
        favorites = favorites_model.get_all_favorites(int(user_id))
        return jsonify({"favorites": favorites}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/weather/current', methods=['GET'])
def get_weather():
    """Fetch current weather for a specific city."""
    user_id = request.args.get('user_id')
    city_name = request.args.get('city_name')

    if not all([user_id, city_name]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        favorites = favorites_model.get_all_favorites(int(user_id))
        favorite = next((fav for fav in favorites if fav["city_name"] == city_name), None)
        if not favorite:
            raise ValueError(f"City {city_name} not in favorites.")

        weather = favorites_model.get_weather(
            city_name, favorite["latitude"], favorite["longitude"], API_KEY
        )
        return jsonify({"weather": weather}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/weather/forecast', methods=['GET'])
def get_forecast():
    """Fetch weather forecast for a specific city."""
    user_id = request.args.get('user_id')
    city_name = request.args.get('city_name')

    if not all([user_id, city_name]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        favorites = favorites_model.get_all_favorites(int(user_id))
        favorite = next((fav for fav in favorites if fav["city_name"] == city_name), None)
        if not favorite:
            raise ValueError(f"City {city_name} not in favorites.")

        forecast = favorites_model.get_forecast(
            city_name, favorite["latitude"], favorite["longitude"], API_KEY
        )
        return jsonify({"forecast": forecast}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/weather/air_pollution', methods=['GET'])
def get_air_pollution():
    """Fetch air pollution data for a specific city."""
    user_id = request.args.get('user_id')
    city_name = request.args.get('city_name')

    if not all([user_id, city_name]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        favorites = favorites_model.get_all_favorites(int(user_id))
        favorite = next((fav for fav in favorites if fav["city_name"] == city_name), None)
        if not favorite:
            raise ValueError(f"City {city_name} not in favorites.")

        air_pollution = favorites_model.get_air_pollution(
            favorite["latitude"], favorite["longitude"], API_KEY
        )
        return jsonify({"air_pollution": air_pollution}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/weather/all', methods=['GET'])
def get_all_weather():
    """Fetch current weather for all favorite cities for a user."""
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "Missing required field: user_id"}), 400

    try:
        # Get all favorite cities for the user
        favorites = favorites_model.get_all_favorites(int(user_id))
        if not favorites:
            return jsonify({"error": "No favorites found for user"}), 404

        # Fetch current weather for all favorites
        all_weather = {}
        for favorite in favorites:
            weather = favorites_model.get_weather(
                favorite["city_name"], favorite["latitude"], favorite["longitude"], API_KEY
            )
            all_weather[favorite["city_name"]] = weather

        return jsonify({"all_weather": all_weather}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/weather/map', methods=['GET'])
def get_weather_map():
    """Fetch specific weather criteria for a city."""
    user_id = request.args.get('user_id')
    city_name = request.args.get('city_name')
    criteria = request.args.get('criteria')

    if not all([user_id, city_name, criteria]):
        return jsonify({"error": "Missing required fields: user_id, city_name, or criteria"}), 400

    try:
        # Validate user and city
        favorites = favorites_model.get_all_favorites(int(user_id))
        favorite = next((fav for fav in favorites if fav["city_name"] == city_name), None)
        if not favorite:
            raise ValueError(f"City {city_name} not in favorites.")

        # Fetch specific weather criteria
        weather_map = favorites_model.get_weather_map(
            city_name, favorite["latitude"], favorite["longitude"], criteria, API_KEY
        )
        return jsonify({"weather_map": weather_map}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
