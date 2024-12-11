from flask import Flask, request, jsonify
from favorite_list_model import FavoriteListModel

app = Flask(__name__)
favorites_model = FavoriteListModel()
API_KEY = "your_openweathermap_api_key"  # Replace with your actual API key

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
