#!/bin/bash

DB_PATH="fitness_tracker.db"

# Check if the database file already exists
if [ -f "$DB_PATH" ]; then
    echo "Database already exists at $DB_PATH."
else
    echo "Creating database at $DB_PATH."
    # Create the database for the first time and create tables
    sqlite3 "$DB_PATH" < ./sql/create_user_table.sql
    echo "Database created successfully."
fi