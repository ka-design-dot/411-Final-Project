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
5. **Get Historical Weather for a Favorite**
   - Retrieve weather data for past days for analysis or record-keeping.
6. **Get Forecast for a Favorite**
   - View detailed weather forecasts for saved locations, including temperature trends and precipitation chances.

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

### 1. Health Check
- **Path:** `/api/health`
- **Request Type:** `GET`
- **Purpose:** Check if the service is running.
- **Example:**
  ```bash
  curl -X GET http://localhost:5000/api/health
  ```
  **Response:**
  ```json
  { "status": "healthy" }
  ```

### 2. Create Account
- **Path:** `/auth/create-account`
- **Request Type:** `POST`
- **Purpose:** Create a new user account.
- **Request Body:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response:**
  ```json
  { "message": "Account created successfully" }
  ```

### 3. Add Favorite Location
- **Path:** `/favorites/add`
- **Request Type:** `POST`
- **Purpose:** Add a city to a user’s favorites.
- **Request Body:**
  ```json
  {
    "user_id": "integer",
    "city_name": "string"
  }
  ```
- **Response:**
  ```json
  { "message": "City added to favorites" }
  ```

### 4. Get All Favorites
- **Path:** `/favorites`
- **Request Type:** `GET`
- **Purpose:** Retrieve all favorite cities for a user.
- **Query Parameters:**
  - `user_id` (integer): ID of the user.
- **Example:**
  ```bash
  curl -X GET "http://localhost:5000/favorites?user_id=1"
  ```
  **Response:**
  ```json
  {
    "favorites": [
      { "city_name": "New York", "latitude": 40.7128, "longitude": -74.0060 },
      { "city_name": "Los Angeles", "latitude": 34.0522, "longitude": -118.2437 }
    ]
  }
  ```

### 5. Get Current Weather
- **Path:** `/weather`
- **Request Type:** `GET`
- **Purpose:** Fetch current weather for a specific city.
- **Query Parameters:**
  - `user_id` (integer): ID of the user.
  - `city_name` (string): Name of the city.
- **Response:**
  ```json
  {
    "weather": {
      "temperature": "float",
      "humidity": "integer",
      "wind_speed": "float"
    }
  }
  ```

### 6. Get Weather Forecast
- **Path:** `/forecast`
- **Request Type:** `GET`
- **Purpose:** Fetch weather forecast for a specific city.
- **Response:**
  ```json
  {
    "forecast": [
      { "day": "Monday", "temperature": "float", "conditions": "string" },
      { "day": "Tuesday", "temperature": "float", "conditions": "string" }
    ]
  }
  ```

---

## Testing

### Unit Tests
1. 

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
