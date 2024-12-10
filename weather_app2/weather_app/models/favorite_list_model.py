import logging
import requests


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class FavoriteListModel:
    def __init__(self):
        """Initialize the model with in-memory storage for favorite cities."""
        self.favorites = {}  # Structure: {user_id: [{"city_name": str, "latitude": float, "longitude": float}]}

    def add_city(self, user_id: int, city_name: str, latitude: float, longitude: float):
        """Add a city to the user's favorites in memory."""
        if user_id not in self.favorites:
            self.favorites[user_id] = []

        # Check if the city already exists in the user's favorites
        for favorite in self.favorites[user_id]:
            if favorite["city_name"] == city_name:
                logger.error("City %s already exists in favorites for user ID %d.", city_name, user_id)
                raise ValueError(f"City {city_name} is already in favorites.")

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
    
    def get_weather_map(self, city_name: str, latitude: float, longitude: float, criteria: str, api_key: str) -> dict:
        """Fetch specific weather information for a city based on given criteria."""
        allowed_criteria = ["clouds", "precipitation", "sea_level_pressure", "wind_speed", "temperature"]
        if criteria not in allowed_criteria:
            raise ValueError(f"Invalid criteria: {criteria}. Allowed criteria are {allowed_criteria}.")

        # Fetch current weather data for the city
        weather_data = self._make_api_call(
            "weather",
            {"lat": latitude, "lon": longitude, "q": city_name},
            api_key
        )

        # Map the requested criteria to the relevant weather data
        criteria_mapping = {
            "clouds": weather_data.get("clouds", {}).get("all"),
            "precipitation": weather_data.get("rain", {}).get("1h") or weather_data.get("snow", {}).get("1h"),
            "sea_level_pressure": weather_data.get("main", {}).get("pressure"),
            "wind_speed": weather_data.get("wind", {}).get("speed"),
            "temperature": weather_data.get("main", {}).get("temp")
        }

        # Extract and return the data for the specified criteria
        result = {criteria: criteria_mapping.get(criteria)}
        if result[criteria] is None:
            logger.warning("Data for criteria %s is not available for city %s.", criteria, city_name)

        logger.info("Weather map for %s (%s): %s", city_name, criteria, result)
        return result
    
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