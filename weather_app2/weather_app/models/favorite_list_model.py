import logging
import requests


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class FavoriteListModel:
    def __init__(self):
        """Initialize the model with in-memory storage for favorite cities."""
        self.favorites = {}  # Structure: {user_id: [{"city_name": str, "latitude": float, "longitude": float}]}

    def add_city(self, user_id: int, city_name: str, api_key: str):
        """
        Add a city to the user's favorites in memory.
        This now uses the geocoding API to determine the latitude and longitude from the city name.
        """
        if user_id not in self.favorites:
            self.favorites[user_id] = []

        # Check if the city already exists in the user's favorites
        for favorite in self.favorites[user_id]:
            if favorite["city_name"] == city_name:
                logger.error("City %s already exists in favorites for user ID %d.", city_name, user_id)
                raise ValueError(f"City {city_name} is already in favorites.")

        # Get the coordinates from the geocoding API
        latitude, longitude = self.get_city_coordinates(city_name, api_key)

        # Add the city to the favorites
        self.favorites[user_id].append({"city_name": city_name, "latitude": latitude, "longitude": longitude})
        logger.info("City %s added to favorites for user ID %d.", city_name, user_id)

    def remove_city(self, user_id: int, city_name: str):
        """Remove a city from the user's favorites in memory."""
        if user_id not in self.favorites or not any(fav["city_name"] == city_name for fav in self.favorites[user_id]):
            logger.error("City %s not found in favorites for user ID %d.", city_name, user_id)
            raise ValueError(f"City {city_name} is not in favorites.")

        # Remove the city from the favorites
        self.favorites[user_id] = [
            fav for fav in self.favorites[user_id] if fav["city_name"] != city_name
        ]
        logger.info("City %s removed from favorites for user ID %d.", city_name, user_id)

    def get_all_favorites(self, user_id: int):
        """Retrieve all favorite cities for a user."""
        favorites = self.favorites.get(user_id, [])
        logger.info("Retrieved favorites for user ID %d: %s", user_id, favorites)
        return favorites

    def _make_api_call(self, endpoint: str, params: dict, api_key: str) -> dict:
        """Helper function to make API calls."""
        base_url = "https://api.openweathermap.org/data/2.5"
        url = f"{base_url}/{endpoint}"
        params["appid"] = api_key

        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            logger.info("API call to %s successful: %s", endpoint, data)
            return data
        except requests.exceptions.RequestException as e:
            logger.error("API call failed: %s", e)
            raise RuntimeError(f"API call failed: {e}")
    
    def _make_geo_api_call(self, city_name: str, api_key: str) -> list:
        """Helper function to make API calls to the geocoding endpoint."""
        base_url = "http://api.openweathermap.org/geo/1.0"
        url = f"{base_url}/direct"
        params = {
            "q": city_name,
            "limit": 1,
            "appid": api_key
        }

        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            logger.info("Geocoding API call successful for city %s: %s", city_name, data)
            return data
        except requests.exceptions.RequestException as e:
            logger.error("Geocoding API call failed: %s", e)
            raise RuntimeError(f"Geocoding API call failed: {e}")

    def get_city_coordinates(self, city_name: str, api_key: str):
        """Get the latitude and longitude for a given city using the geocoding API."""
        data = self._make_geo_api_call(city_name, api_key)
        if not data:
            logger.error("No coordinates found for city %s.", city_name)
            raise ValueError(f"No coordinates found for city {city_name}.")
        lat = data[0].get("lat")
        lon = data[0].get("lon")
        if lat is None or lon is None:
            logger.error("Incomplete data returned for city %s.", city_name)
            raise ValueError(f"Incomplete coordinate data for city {city_name}.")
        return lat, lon

    def get_weather(self, user_id: int, city_name: str, api_key: str):
        """Fetch current weather for a specific city."""
        favorites = self.favorites.get(user_id, [])
        for favorite in favorites:
            if favorite["city_name"] == city_name:
                return self._make_api_call(
                    "weather",
                    {"lat": favorite["latitude"], "lon": favorite["longitude"]},
                    api_key
                )

        logger.error("City %s not found in favorites for user ID %d.", city_name, user_id)
        raise ValueError(f"City {city_name} is not in favorites.")

    def get_all_weather(self, user_id: int, api_key: str):
        """Fetch weather for all favorite cities for a user."""
        favorites = self.favorites.get(user_id, [])
        weather_data = {}

        for favorite in favorites:
            weather_data[favorite["city_name"]] = self._make_api_call(
                "weather",
                {"lat": favorite["latitude"], "lon": favorite["longitude"]},
                api_key
            )

        logger.info("Retrieved weather for all favorites for user ID %d.", user_id)
        return weather_data
    
    def get_weather_map(self, user_id: int, city_name: str, criteria: str, api_key: str) -> dict:
        """
        Fetch a weather layer tile for a city in the user's favorites based on the given criteria.

        Criteria to layer mapping:
        - clouds -> clouds_new
        - precipitation -> precipitation_new
        - sea_level_pressure -> pressure_new
        - wind_speed -> wind_new
        - temperature -> temp_new
        """
        favorites = self.favorites.get(user_id, [])
        for favorite in favorites:
            if favorite["city_name"] == city_name:
                allowed_criteria = ["clouds", "precipitation", "sea_level_pressure", "wind_speed", "temperature"]
                if criteria not in allowed_criteria:
                    logger.error("Invalid criteria %s requested for city %s by user ID %d.", criteria, city_name, user_id)
                    raise ValueError(f"Invalid criteria: {criteria}. Allowed criteria are {allowed_criteria}.")

                criteria_to_layer = {
                    "clouds": "clouds_new",
                    "precipitation": "precipitation_new",
                    "sea_level_pressure": "pressure_new",
                    "wind_speed": "wind_new",
                    "temperature": "temp_new"
                }

                layer = criteria_to_layer[criteria]

                # Choose a zoom level. This can be adjusted as needed.
                z = 5

                # Convert latitude/longitude to tile coordinates for the chosen zoom level.
                import math
                latitude = favorite["latitude"]
                longitude = favorite["longitude"]
                lat_rad = math.radians(latitude)
                n = 2 ** z  # number of tiles at this zoom level

                x = (longitude + 180.0) / 360.0 * n
                y = (1.0 - math.log(math.tan(lat_rad) + (1.0 / math.cos(lat_rad))) / math.pi) / 2.0 * n

                # Convert to int and clamp to valid range [0, 2^z - 1]
                x = int(min(max(x, 0), n - 1))
                y = int(min(max(y, 0), n - 1))

                tile_url = f"https://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?appid={api_key}"

                logger.info("Weather map tile URL for city %s (user ID %d, %s): %s", city_name, user_id, criteria, tile_url)

                return {
                    "criteria": criteria,
                    "layer": layer,
                    "zoom": z,
                    "x": x,
                    "y": y,
                    "tile_url": tile_url
                }

        logger.error("City %s not found in favorites for user ID %d.", city_name, user_id)
        raise ValueError(f"City {city_name} is not in favorites.")
    
    def get_forecast(self, user_id: int, city_name: str, api_key: str):
        """Fetch the weather forecast for a specific city."""
        favorites = self.favorites.get(user_id, [])
        for favorite in favorites:
            if favorite["city_name"] == city_name:
                forecast_data = self._make_api_call(
                    "forecast",
                    {"lat": favorite["latitude"], "lon": favorite["longitude"]},
                    api_key
                )
                logger.info("Retrieved forecast for city %s for user ID %d: %s", city_name, user_id, forecast_data)
                return forecast_data

        logger.error("City %s not found in favorites for user ID %d.", city_name, user_id)
        raise ValueError(f"City {city_name} is not in favorites.")

    def get_air_pollution(self, user_id: int, city_name: str, api_key: str):
        """Fetch air pollution data for a city in the user's favorites."""
        favorites = self.favorites.get(user_id, [])
        for favorite in favorites:
            if favorite["city_name"] == city_name:
                air_pollution_data = self._make_api_call(
                    "air_pollution",
                    {"lat": favorite["latitude"], "lon": favorite["longitude"]},
                    api_key
                )
                logger.info("Retrieved air pollution data for city %s for user ID %d: %s", city_name, user_id, air_pollution_data)
                return air_pollution_data

        logger.error("City %s not found in favorites for user ID %d.", city_name, user_id)
        raise ValueError(f"City {city_name} is not in favorites.")