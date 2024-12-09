import os
import sqlite3
from flask import Flask, jsonify, request
from werkzeug.exceptions import NotFound
from logger.py import configure_logger  # Import the configure_logger from your logger file

app = Flask(__name__)

# Set up the logger using your pre-configured logger
configure_logger(app.logger)

# Database configuration
DATABASE = 'fitness_tracker.db'

def get_db():
    """ Get a connection to the database """
    conn = sqlite3.connect(DATABASE)
    return conn

def init_db():
    """ Initialize the database by running SQL commands from the user.sql file """
    with sqlite3.connect(DATABASE) as conn:
        with open('user.sql', 'r') as sql_file:
            sql_script = sql_file.read()
        conn.executescript(sql_script)
        app.logger.info("Database initialized from user.sql")

@app.before_first_request
def before_first_request():
    """ Initialize the database the first time the app is run """
    if not os.path.exists(DATABASE):
        init_db()
        app.logger.info(f"Database {DATABASE} created successfully.")
    else:
        app.logger.info(f"Database {DATABASE} already exists.")

@app.route('/api/health', methods=['GET'])
def healthcheck():
    """ Health check route to verify the service is running """
    app.logger.info('Health check')
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/create-account', methods=['POST'])
def create_account():
    """ Route to create a new user account """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Here you'd normally hash the password and save the user to the database
    app.logger.debug(f"Attempting to create account for {username}")

    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, password))
            conn.commit()
        app.logger.info(f"Account created for {username}")
        return jsonify({"message": "Account created successfully"}), 201
    except Exception as e:
        app.logger.error(f"Error creating account for {username}: {str(e)}")
        return jsonify({"message": "An error occurred. Please try again later."}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """ Route to login a user """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    app.logger.debug(f"Attempting to log in user {username}")

    # Here you'd normally check the hashed password
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM users WHERE username = ? AND password = ?''', (username, password))
            user = cursor.fetchone()
            
            if user:
                app.logger.info(f"User {username} logged in successfully.")
                return jsonify({"message": "Login successful"}), 200
            else:
                app.logger.warning(f"Failed login attempt for {username}")
                return jsonify({"message": "Invalid username or password"}), 401
    except Exception as e:
        app.logger.error(f"Error logging in user {username}: {str(e)}")
        return jsonify({"message": "An error occurred. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True)