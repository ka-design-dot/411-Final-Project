
from flask import Flask, request, jsonify
from weather_app.models.favorite_list_model import FavoriteListModel

app = Flask(__name__)
favorites_model = FavoriteListModel()
API_KEY = #"your_openweathermap_api_key"  # Replace with your actual API key

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
