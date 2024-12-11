import unittest
from unittest.mock import patch, MagicMock
from weather_app.models.favorite_list_model import FavoriteListModel


class TestFavoriteListModel(unittest.TestCase):

    def setUp(self):
        self.model = FavoriteListModel()
        self.user_id = 1
        self.city_name = "TestCity"
        self.api_key = "test_api_key"

    @patch("favorite_list_model.FavoriteListModel._make_geo_api_call")
    def test_add_city(self, mock_geo_api_call):
        # Mock geocoding API response
        mock_geo_api_call.return_value = [{"lat": 10.0, "lon": 20.0}]

        self.model.add_city(self.user_id, self.city_name, self.api_key)

        # Verify the city was added
        favorites = self.model.get_all_favorites(self.user_id)
        self.assertEqual(len(favorites), 1)
        self.assertEqual(favorites[0]["city_name"], self.city_name)
        self.assertEqual(favorites[0]["latitude"], 10.0)
        self.assertEqual(favorites[0]["longitude"], 20.0)

    @patch("favorite_list_model.FavoriteListModel._make_geo_api_call")
    def test_add_duplicate_city_raises_error(self, mock_geo_api_call):
        mock_geo_api_call.return_value = [{"lat": 10.0, "lon": 20.0}]

        self.model.add_city(self.user_id, self.city_name, self.api_key)

        with self.assertRaises(ValueError):
            self.model.add_city(self.user_id, self.city_name, self.api_key)

    def test_remove_city(self):
        self.model.favorites = {
            self.user_id: [{"city_name": self.city_name, "latitude": 10.0, "longitude": 20.0}]
        }

        self.model.remove_city(self.user_id, self.city_name)

        # Verify the city was removed
        favorites = self.model.get_all_favorites(self.user_id)
        self.assertEqual(len(favorites), 0)

    def test_remove_nonexistent_city_raises_error(self):
        with self.assertRaises(ValueError):
            self.model.remove_city(self.user_id, self.city_name)

    def test_get_all_favorites(self):
        self.model.favorites = {
            self.user_id: [
                {"city_name": self.city_name, "latitude": 10.0, "longitude": 20.0},
                {"city_name": "AnotherCity", "latitude": 30.0, "longitude": 40.0},
            ]
        }

        favorites = self.model.get_all_favorites(self.user_id)
        self.assertEqual(len(favorites), 2)
        self.assertEqual(favorites[0]["city_name"], self.city_name)
        self.assertEqual(favorites[1]["city_name"], "AnotherCity")

    @patch("favorite_list_model.FavoriteListModel._make_api_call")
    def test_get_weather(self, mock_api_call):
        # Mock weather API response
        mock_api_call.return_value = {"weather": "sunny"}

        self.model.favorites = {
            self.user_id: [{"city_name": self.city_name, "latitude": 10.0, "longitude": 20.0}]
        }

        weather = self.model.get_weather(self.user_id, self.city_name, self.api_key)
        self.assertEqual(weather, {"weather": "sunny"})

    @patch("favorite_list_model.FavoriteListModel._make_api_call")
    def test_get_all_weather(self, mock_api_call):
        # Mock weather API response
        mock_api_call.return_value = {"weather": "sunny"}

        self.model.favorites = {
            self.user_id: [
                {"city_name": self.city_name, "latitude": 10.0, "longitude": 20.0},
                {"city_name": "AnotherCity", "latitude": 30.0, "longitude": 40.0},
            ]
        }

        weather_data = self.model.get_all_weather(self.user_id, self.api_key)
        self.assertEqual(len(weather_data), 2)
        self.assertIn(self.city_name, weather_data)
        self.assertIn("AnotherCity", weather_data)

    @patch("favorite_list_model.FavoriteListModel._make_api_call")
    def test_get_air_pollution(self, mock_api_call):
        # Mock air pollution API response
        mock_api_call.return_value = {"pollution": "low"}

        self.model.favorites = {
            self.user_id: [{"city_name": self.city_name, "latitude": 10.0, "longitude": 20.0}]
        }

        pollution_data = self.model.get_air_pollution(self.user_id, self.city_name, self.api_key)
        self.assertEqual(pollution_data, {"pollution": "low"})

    def test_get_air_pollution_no_city(self):
        with self.assertRaises(ValueError):
            self.model.get_air_pollution(self.user_id, "NonExistentCity", self.api_key)

    def test_get_weather_no_city(self):
        with self.assertRaises(ValueError):
            self.model.get_weather(self.user_id, "NonExistentCity", self.api_key)

if __name__ == "__main__":
    unittest.main()
