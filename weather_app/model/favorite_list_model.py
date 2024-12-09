from dataclasses import dataclass
import logging
import os
import sqlite3
from db import db
from flask import Flask, jsonify, request, Response, make_response
import requests
from dotenv import load_dotenv

from weather_app.utils.logger import configure_logger
from weather_app.utils.sql_utils import get_db_connection

load_dotenv()

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

logger = logging.getLogger(__name__)
configure_logger(logger)

@dataclass
class FavoriteLocation:
    id: int
    user_id: int
    name: str
    lat: float
    lon: float

    def __post_init__(self):

        if not (-90 <= self.lat <= 90):
            raise ValueError(f"Invalid latitude: {self.lat} (must be between -90 and 90).")
        if not (-180 <= self.lon <= 180):
            raise ValueError(f"Invalid longitude: {self.lon} (must be between -180 and 180).")

    
# def create_favorite_city(user_id: int, name: str, lat: float, lon: float) -> None: #will work later with geocoding to make use of the lat and lon
#     """
#     Creates a new favorite city for a user in the favorite_cities table.

#     Args:
#         user_id (int): The user's ID.
#         name (str): Name of the city.
#         lat (float): Latitude of the city.
#         lon (float): Longitude of the city.

#     Raises:
#         ValueError: If latitude or longitude are invalid.
#         sqlite3.IntegrityError: If the city already exists for the user.
#         sqlite3.Error: For any other database errors.
#     """
#     if not (-90 <= lat <= 90):
#         raise ValueError(f"Invalid latitude: {lat} (must be between -90 and 90).")
#     if not (-180 <= lon <= 180):
#         raise ValueError(f"Invalid longitude: {lon} (must be between -180 and 180).")

#     try:
#         with get_db_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute("""
#                 INSERT INTO favorite_cities (user_id, name, lat, lon)
#                 VALUES (?, ?, ?, ?)
#             """, (user_id, name, lat, lon))
#             conn.commit()

#             logger.info("Favorite city created successfully for user_id %s: %s", user_id, name)

#     except sqlite3.IntegrityError as e:
#         logger.error("City '%s' already exists for user_id %s.", name, user_id)
#         raise ValueError(f"City '{name}' already exists for user_id {user_id}.") from e
#     except sqlite3.Error as e:
#         logger.error("Database error while creating favorite city: %s", str(e))
#         raise sqlite3.Error(f"Database error: {str(e)}")

# def delete_favorite_city(city_id: int) -> None:
#     """
#     Deletes a favorite city from the favorite_cities table.

#     Args:
#         city_id (int): The ID of the city to delete.

#     Raises:
#         ValueError: If the city ID does not exist.
#         sqlite3.Error: For any database errors.
#     """
#     try:
#         with get_db_connection() as conn:
#             cursor = conn.cursor()

#             # Verify the city exists
#             cursor.execute("SELECT id FROM favorite_cities WHERE id = ?", (city_id,))
#             if cursor.fetchone() is None:
#                 logger.info("City with ID %s not found.", city_id)
#                 raise ValueError(f"City with ID {city_id} not found.")

#             # Delete the city
#             cursor.execute("DELETE FROM favorite_cities WHERE id = ?", (city_id,))
#             conn.commit()

#             logger.info("City with ID %s deleted successfully.", city_id)

#     except sqlite3.Error as e:
#         logger.error("Database error while deleting city: %s", str(e))
#         raise e
    
# def get_favorite_cities(user_id: int) -> list[FavoriteCity]:
#     """
#     Retrieves all favorite cities for a given user.

#     Args:
#         user_id (int): The user's ID.

#     Returns:
#         list[FavoriteCity]: A list of the user's favorite cities.

#     Raises:
#         sqlite3.Error: For any database errors.
#     """
#     try:
#         with get_db_connection() as conn:
#             cursor = conn.cursor()
#             rows = cursor.execute("""
#                 SELECT id, user_id, name, lat, lon
#                 FROM favorite_cities
#                 WHERE user_id = ?
#             """, (user_id,)).fetchall()

#             favorite_cities = [FavoriteCity(*row) for row in rows]

#             logger.info("Retrieved %d favorite cities for user_id %s.", len(favorite_cities), user_id)

#             return favorite_cities

#     except sqlite3.Error as e:
#         logger.error("Database error while retrieving favorite cities for user_id %s: %s", user_id, str(e))
#         raise e
    
#########################################################################################################################
    
    #1. Set Favorite Locations
def add_favorite_location(user_id, location):
    """
    Add a favorite location for the user.
    Args:
        user_id (int): The ID of the user.
        location (str): The name of the location to add.

    Returns:
        dict: A success or error message.
    """
    # Check if the location already exists for the user
    existing_favorite = FavoriteLocation.query.filter_by(user_id=user_id, location=location).first()
    if existing_favorite:
        return {'error': 'Location already exists in favorites'}

    # Add the new favorite location
    new_favorite = FavoriteLocation(user_id=user_id, location=location)
    db.session.add(new_favorite)
    db.session.commit()

    return {'message': 'Favorite location added successfully'}

#2. Get Weather for a Favorite Location
def get_weather(location):
    """
    Get current weather for a given location.
    Args:
        location (str): The location for which weather data is requested.

    Returns:
        dict: Weather data or an error message.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        return {
            'location': location,
            'temperature': weather_data['main']['temp'],
            'humidity': weather_data['main']['humidity'],
            'wind_speed': weather_data['wind']['speed'],
            'description': weather_data['weather'][0]['description']
        }
    else:
        return {'error': 'Could not fetch weather data'}

#3. View All Favorites with Current Weather
def view_favorites_weather(user_id):
    """
    Get the current weather for all of a user's favorite locations.
    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of weather data for all favorite locations.
    """
    favorites = FavoriteLocation.query.filter_by(user_id=user_id).all()
    results = []

    for favorite in favorites:
        weather = get_weather(favorite.location)
        if 'error' not in weather:
            results.append({
                'location': favorite.location,
                'temperature': weather['temperature'],
                'description': weather['description']
            })
        else:
            results.append({'location': favorite.location, 'error': weather['error']})

    return results

#4. See All Favorites
def view_favorites(user_id):
    """
    Get all favorite locations for a user.
    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of favorite locations.
    """
    favorites = FavoriteLocation.query.filter_by(user_id=user_id).all()
    return [favorite.location for favorite in favorites]

#5. Get Historical Weather for a Favorite
def get_historical_weather(location, timestamp):
    """
    Get historical weather for a given location and timestamp.
    Args:
        location (str): The location for which historical weather data is requested.
        timestamp (int): UNIX timestamp for the historical weather data.

    Returns:
        dict: Historical weather data or an error message.
    """
    # Note: OpenWeatherMap API requires lat/lon for historical data
    # You may need to fetch coordinates for the location
    lat, lon = get_coordinates(location)  # Implement this helper function
    url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={timestamp}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Could not fetch historical weather data'}

#6. Get Forecast for a Favorite
def get_forecast(location):
    """
    Get weather forecast for a given location.
    Args:
        location (str): The location for which the weather forecast is requested.

    Returns:
        list: A list of forecast data for the next few days or an error message.
    """
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        forecast_data = response.json()
        forecasts = [
            {
                'date': item['dt_txt'],
                'temperature': item['main']['temp'],
                'description': item['weather'][0]['description']
            }
            for item in forecast_data['list']
        ]
        return forecasts
    else:
        return {'error': 'Could not fetch forecast data'}


def get_coordinates(location):
    """
    Get latitude and longitude for a given location (placeholder).
    Args:
        location (str): The name of the location.

    Returns:
        tuple: Latitude and longitude.
    """
    # Implement a real geocoding API call if needed
    # Example return values
    return (40.7128, -74.0060)  # Placeholder coordinates for New York City