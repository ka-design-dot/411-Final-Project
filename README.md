# Weather Dashboard Application

## Overview
The Weather Dashboard is a web-based application designed to provide users with personalized weather information. Users can save favorite locations and easily access current, forecasted, and historical weather data. By leveraging the OpenWeatherMap API, the application delivers user-specific customization, making it easier to stay informed about weather conditions in areas of interest.

---

## Features

1. **Set Favorite Locations**
   - Add and save favorite locations to a user’s profile for quick access.
2. **Get Weather for a Favorite Location**
   - Retrieve current weather details for a user’s saved location, including temperature, humidity, and wind speed.
3. **View All Favorites with Current Weather**
   - Display all saved locations with their current weather conditions.
4. **See All Favorites**
   - View a list of all saved locations for management or selection purposes.
5. **Get Forecast for a Favorite**
   - View detailed weather forecasts for saved locations, including temperature trends and precipitation chances.
6. **Detect Air Pollution**
   - Retrieve air quality data, including pollution levels, for saved locations to stay informed about environmental conditions.
7. **Weather Map**
   - Visualize specific weather conditions (e.g., clouds, precipitation, sea level pressure, wind speed, temperature) for a saved location based on selected criteria.

---

## Setup Instructions

### Using Docker
1. Build the Docker image:
   ```bash
   docker build -t weather_app:0.2.0 .
   ```
2. Run the Docker container:
   ```bash
   docker run -d \
     --name weather_app_container \
     --env-file .env \
     -p 5000:5000 \
     -v ./db:/app/db \
     weather_app:0.2.0
   ```
3. Access the application at `http://localhost:5000`.

### Local Development
1. Set up a virtual environment:
   ```bash
   ./setup_venv.sh
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   export DB_PATH=./db/weather_app.db
   ./create_db.sh
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Access the application at `http://localhost:5000`.

---

## Database Configuration

- **Default Path:** The SQLite database file is located at `/app/sql/weather_app.db`. You can override this path by setting the `DB_PATH` environment variable.
- **Initialization Script:** The database is initialized with the schema defined in `create_user_table.sql`. Use the `create_db.sh` script to create or reset the database.

---

## Logging

The application uses a centralized logging system for debugging and monitoring:
- Logs are written to the console with timestamps and log levels.
- Configure the logger in `logger.py` to adjust logging levels or formats.
- Key events such as API calls, database operations, and error messages are logged.

---

## API Routes

### Route: /api/health
● Request Type: GET
● Purpose: Checks if the service is running.
● Response Format: JSON
  ○ Success Response Example:
    ■ Code: 200
    ■ Content: { "status": "healthy" }
● Example Request:
```bash
curl -X GET http://localhost:5000/api/health
```
● Example Response:
```json
{
  "status": "healthy"
}
```

### Route: /auth/create-account
● Request Type: POST
● Purpose: Creates a new user account with a username and password.
● Request Body:
  ○ username (String): User's chosen username.
  ○ password (String): User's chosen password.
● Response Format: JSON
  ○ Success Response Example:
    ■ Code: 201
    ■ Content: { "message": "Account created successfully" }
● Example Request:
```json
{
  "username": "newuser123",
  "password": "securepassword"
}
```
● Example Response:
```json
{
  "message": "Account created successfully"
}
```

### Route: /favorites/add
● Request Type: POST
● Purpose: Adds a city to a user’s favorites.
● Request Body:
  ○ user_id (Integer): ID of the user.
  ○ city_name (String): Name of the city to be added.
● Response Format: JSON
  ○ Success Response Example:
    ■ Code: 200
    ■ Content: { "message": "City added to favorites" }
● Example Request:
```json
{
  "user_id": 1,
  "city_name": "New York"
}
```
● Example Response:
```json
{
  "message": "City added to favorites"
}
```

### Route: /favorites
● Request Type: GET
● Purpose: Retrieves all favorite cities for a user.
● Query Parameters:
  ○ user_id (Integer): ID of the user.
● Response Format: JSON
  ○ Success Response Example:
    ■ Code: 200
    ■ Content: { "favorites": [ { "city_name": "New York", "latitude": 40.7128, "longitude": -74.0060 } ] }
● Example Request:
```bash
curl -X GET "http://localhost:5000/favorites?user_id=1"
```
● Example Response:
```json
{
  "favorites": [
    {
      "city_name": "New York",
      "latitude": 40.7128,
      "longitude": -74.0060
    }
  ]
}
```

### Route: /weather
● Request Type: GET
● Purpose: Fetches current weather for a specific city.
● Query Parameters:
  ○ user_id (Integer): ID of the user.
  ○ city_name (String): Name of the city.
● Response Format: JSON
  ○ Success Response Example:
    ■ Code: 200
    ■ Content: { "weather": { "temperature": 22.5, "humidity": 60, "wind_speed": 5.2 } }
● Example Request:
```bash
curl -X GET "http://localhost:5000/weather?user_id=1&city_name=New+York"
```
● Example Response:
```json
{
  "weather": {
    "temperature": 22.5,
    "humidity": 60,
    "wind_speed": 5.2
  }
}
```

### Route: /forecast
● Request Type: GET
● Purpose: Fetches weather forecast for a specific city.
● Query Parameters:
  ○ user_id (Integer): ID of the user.
  ○ city_name (String): Name of the city.
● Response Format: JSON
  ○ Success Response Example:
    ■ Code: 200
    ■ Content: { "forecast": [ { "day": "Monday", "temperature": 20.5 }, { "day": "Tuesday", "temperature": 22.0 } ] }
● Example Request:
```bash
curl -X GET "http://localhost:5000/forecast?user_id=1&city_name=New+York"
```
● Example Response:
```json
{
  "forecast": [
    { "day": "Monday", "temperature": 20.5 },
    { "day": "Tuesday", "temperature": 22.0 }
  ]
}
```

---

## Testing

### Unit Tests
Unit tests ensure that individual components of the application work as expected. They are located in the `tests` directory.

#### Running Unit Tests
1. Activate the virtual environment:
   ```bash
   source weather_app_venv/bin/activate
   ```
2. Run the tests using `pytest`:
   ```bash
   pytest tests
   ```

### Smoke Tests
Smoke tests verify that the critical paths of the application are functioning correctly. These include API endpoint tests and basic workflows.

#### Running Smoke Tests
1. Build and start the Docker container:
   ```bash
   ./run_docker.sh
   ```
2. Run the smoke tests script:
   ```bash
   ./smoketest.sh
   ```

The smoke test script runs a series of API calls against the running application to ensure basic functionality.

---

## Commands for Smoke Tests

1. Build and run the Docker container:
   ```bash
   ./run_docker.sh
   ```

2. Run API smoke tests:
   ```bash
   ./smoketest.sh
   ```
