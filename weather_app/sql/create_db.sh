#!/bin/bash

DB_PATH="weather_list.db" #changed the name to match the weather

# Check if the database file already exists
if [ -f "$DB_PATH" ]; then
    echo "Database already exists at $DB_PATH."
else
    echo "Creating database at $DB_PATH."
    # Create the database for the first time and create tables
    sqlite3 "$DB_PATH" < ./sql/create_user_table.sql
    sqlite3 "$DB_PATH" < ./sql/favorite_cities.sql #ADDED for the second database table for the cities
    echo "Database created successfully."
fi

