from flask import Flask, request, jsonify
from favorite_list_model import FavoriteListModel

app = Flask(__name__)
favorites_model = FavoriteListModel()
API_KEY = "3cbb6f2fd7081e9984bc34bafde8e143" #"your_openweathermap_api_key"  # Replace with your actual API key

# @app.route('/favorites/add', methods=['POST'])
# def add_city():
#     """Add a city to the user's favorites."""
#     data = request.json
#     user_id = data.get('user_id')
#     city_name = data.get('city_name')
#     latitude = data.get('latitude')
#     longitude = data.get('longitude')

#     if not all([user_id, city_name, latitude, longitude]):
#         return jsonify({"error": "Missing required fields"}), 400

#     try:
#         favorites_model.add_city(user_id, city_name, latitude, longitude)
#         return jsonify({"message": f"City {city_name} added to favorites"}), 200
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 400

# @app.route('/favorites/remove', methods=['DELETE'])
# def remove_city():
#     """Remove a city from the user's favorites."""
#     data = request.json
#     user_id = data.get('user_id')
#     city_name = data.get('city_name')

#     if not all([user_id, city_name]):
#         return jsonify({"error": "Missing required fields"}), 400

#     try:
#         favorites_model.remove_city(user_id, city_name)
#         return jsonify({"message": f"City {city_name} removed from favorites"}), 200
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 400

# @app.route('/favorites', methods=['GET'])
# def get_all_favorites():
#     """Retrieve all favorite cities for a user."""
#     user_id = request.args.get('user_id')

#     if not user_id:
#         return jsonify({"error": "Missing required field: user_id"}), 400

#     try:
#         favorites = favorites_model.get_all_favorites(int(user_id))
#         return jsonify({"favorites": favorites}), 200
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 400

# @app.route('/weather/current', methods=['GET'])
# def get_weather():
#     """Fetch current weather for a specific city."""
#     user_id = request.args.get('user_id')
#     city_name = request.args.get('city_name')

#     if not all([user_id, city_name]):
#         return jsonify({"error": "Missing required fields"}), 400

#     try:
#         favorites = favorites_model.get_all_favorites(int(user_id))
#         favorite = next((fav for fav in favorites if fav["city_name"] == city_name), None)
#         if not favorite:
#             raise ValueError(f"City {city_name} not in favorites.")

#         weather = favorites_model.get_weather(
#             city_name, favorite["latitude"], favorite["longitude"], API_KEY
#         )
#         return jsonify({"weather": weather}), 200
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 400

# @app.route('/weather/forecast', methods=['GET'])
# def get_forecast():
#     """Fetch weather forecast for a specific city."""
#     user_id = request.args.get('user_id')
#     city_name = request.args.get('city_name')

#     if not all([user_id, city_name]):
#         return jsonify({"error": "Missing required fields"}), 400

#     try:
#         favorites = favorites_model.get_all_favorites(int(user_id))
#         favorite = next((fav for fav in favorites if fav["city_name"] == city_name), None)
#         if not favorite:
#             raise ValueError(f"City {city_name} not in favorites.")

#         forecast = favorites_model.get_forecast(
#             city_name, favorite["latitude"], favorite["longitude"], API_KEY
#         )
#         return jsonify({"forecast": forecast}), 200
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 400

# @app.route('/weather/air_pollution', methods=['GET'])
# def get_air_pollution():
#     """Fetch air pollution data for a specific city."""
#     user_id = request.args.get('user_id')
#     city_name = request.args.get('city_name')

#     if not all([user_id, city_name]):
#         return jsonify({"error": "Missing required fields"}), 400

#     try:
#         favorites = favorites_model.get_all_favorites(int(user_id))
#         favorite = next((fav for fav in favorites if fav["city_name"] == city_name), None)
#         if not favorite:
#             raise ValueError(f"City {city_name} not in favorites.")

#         air_pollution = favorites_model.get_air_pollution(
#             favorite["latitude"], favorite["longitude"], API_KEY
#         )
#         return jsonify({"air_pollution": air_pollution}), 200
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 400

# @app.route('/weather/all', methods=['GET'])
# def get_all_weather():
#     """Fetch current weather for all favorite cities for a user."""
#     user_id = request.args.get('user_id')

#     if not user_id:
#         return jsonify({"error": "Missing required field: user_id"}), 400

#     try:
#         # Get all favorite cities for the user
#         favorites = favorites_model.get_all_favorites(int(user_id))
#         if not favorites:
#             return jsonify({"error": "No favorites found for user"}), 404

#         # Fetch current weather for all favorites
#         all_weather = {}
#         for favorite in favorites:
#             weather = favorites_model.get_weather(
#                 favorite["city_name"], favorite["latitude"], favorite["longitude"], API_KEY
#             )
#             all_weather[favorite["city_name"]] = weather

#         return jsonify({"all_weather": all_weather}), 200
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 400

# @app.route('/weather/map', methods=['GET'])
# def get_weather_map():
#     """Fetch specific weather criteria for a city."""
#     user_id = request.args.get('user_id')
#     city_name = request.args.get('city_name')
#     criteria = request.args.get('criteria')

#     if not all([user_id, city_name, criteria]):
#         return jsonify({"error": "Missing required fields: user_id, city_name, or criteria"}), 400

#     try:
#         # Validate user and city
#         favorites = favorites_model.get_all_favorites(int(user_id))
#         favorite = next((fav for fav in favorites if fav["city_name"] == city_name), None)
#         if not favorite:
#             raise ValueError(f"City {city_name} not in favorites.")

#         # Fetch specific weather criteria
#         weather_map = favorites_model.get_weather_map(
#             city_name, favorite["latitude"], favorite["longitude"], criteria, API_KEY
#         )
#         return jsonify({"weather_map": weather_map}), 200
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 

######################################################################################################

#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000"

##########################################################
# Health Check
##########################################################
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/api/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

##########################################################
# Database Check
##########################################################
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/api/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}

##########################################################
# User Management
##########################################################
create_account() {
  username=$1
  password=$2
  echo "Creating account for $username..."
  curl -s -X POST "$BASE_URL/auth/create-account" -H "Content-Type: application/json" \
    -d '{"username": "$username", "password": "$password"}' | grep -q '"message": "Account created successfully"'
  if [ $? -eq 0 ]; then
    echo "Account created successfully for $username."
  else
    echo "Failed to create account for $username."
    exit 1
  fi
}

login() {
  username=$1
  password=$2
  echo "Logging in $username..."
  curl -s -X POST "$BASE_URL/auth/login" -H "Content-Type: application/json" \
    -d '{"username": "$username", "password": "$password"}' | grep -q '"message": "Login successful"'
  if [ $? -eq 0 ]; then
    echo "$username logged in successfully."
  else
    echo "Failed to log in $username."
    exit 1
  fi
}

update_password() {
  username=$1
  new_password=$2
  echo "Updating password for $username..."
  curl -s -X PUT "$BASE_URL/auth/update-password" -H "Content-Type: application/json" \
    -d '{"username": "$username", "new_password": "$new_password"}' | grep -q '"message": "Password updated successfully"'
  if [ $? -eq 0 ]; then
    echo "Password updated successfully for $username."
  else
    echo "Failed to update password for $username."
    exit 1
  fi
}

##########################################################
# Favorites Management
##########################################################
add_favorite_city() {
  user_id=$1
  city_name=$2
  echo "Adding city $city_name to favorites for user $user_id..."
  curl -s -X POST "$BASE_URL/favorites/add" -H "Content-Type: application/json" \
    -d '{"user_id": $user_id, "city_name": "$city_name"}' | grep -q '"message": "City $city_name added to favorites"'
  if [ $? -eq 0 ]; then
    echo "City $city_name added successfully to user $user_id's favorites."
  else
    echo "Failed to add city $city_name to favorites for user $user_id."
    exit 1
  fi
}

remove_favorite_city() {
  user_id=$1
  city_name=$2
  echo "Removing city $city_name from favorites for user $user_id..."
  curl -s -X DELETE "$BASE_URL/favorites/remove" -H "Content-Type: application/json" \
    -d '{"user_id": $user_id, "city_name": "$city_name"}' | grep -q '"message": "City $city_name removed from favorites"'
  if [ $? -eq 0 ]; then
    echo "City $city_name removed successfully from user $user_id's favorites."
  else
    echo "Failed to remove city $city_name from favorites for user $user_id."
    exit 1
  fi
}

get_favorites() {
  user_id=$1
  echo "Fetching all favorite cities for user $user_id..."
  curl -s -X GET "$BASE_URL/favorites?user_id=$user_id" | grep -q '"favorites"'
  if [ $? -eq 0 ]; then
    echo "Favorites retrieved successfully for user $user_id."
  else
    echo "Failed to retrieve favorites for user $user_id."
    exit 1
  fi
}

get_weather() {
  user_id=$1
  city_name=$2
  echo "Fetching weather for $city_name for user $user_id..."
  curl -s -X GET "$BASE_URL/weather?user_id=$user_id&city_name=$(echo $city_name | sed 's/ /%20/g')" | grep -q '"weather"'
  if [ $? -eq 0 ]; then
    echo "Weather for $city_name retrieved successfully for user $user_id."
  else
    echo "Failed to retrieve weather for $city_name for user $user_id."
    exit 1
  fi
}

get_air_pollution() {
  user_id=$1
  city_name=$2
  echo "Fetching air pollution data for $city_name for user $user_id..."
  curl -s -X GET "$BASE_URL/air_pollution?user_id=$user_id&city_name=$(echo $city_name | sed 's/ /%20/g')" | grep -q '"air_pollution"'
  if [ $? -eq 0 ]; then
    echo "Air pollution data for $city_name retrieved successfully for user $user_id."
  else
    echo "Failed to retrieve air pollution data for $city_name for user $user_id."
    exit 1
  fi
}


get_all_weather() {
  user_id=$1
  echo "Fetching weather for all favorite cities for user $user_id..."
  curl -s -X GET "$BASE_URL/weather/all?user_id=$user_id" | grep -q '"all_weather"'
  if [ $? -eq 0 ]; then
    echo "Weather for all favorite cities retrieved successfully for user $user_id."
  else
    echo "Failed to retrieve weather for all favorite cities for user $user_id."
    exit 1
  fi
}

# Execute Smoketests
check_health
check_db
create_account "testuser" "password123"
login "testuser" "password123"
update_password "testuser" "newpassword123"
add_favorite_city 1 "Los Angeles"
get_favorites 1
get_weather 1 "Los Angeles"
get_air_pollution 1 "Los Angeles"
remove_favorite_city 1 "Los Angeles"
get_all_weather 1

echo "All smoketests passed successfully!"
