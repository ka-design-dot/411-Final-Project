import logging
import os
from werkzeug.security import generate_password_hash, check_password_hash
from utils.sql_utils import get_db_connection
from utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

class UserModel:
    def create_account(self, username: str, password: str):
        """Create a new user account with a hashed password.

        This method creates a new user account by storing the username and a 
        securely hashed version of the password in the database. If the account 
        creation fails, an error is logged, and an exception is raised.

        Parameters
        ----------
        username : str
            The desired username for the new account.
        password : str
            The plaintext password for the account, which will be hashed before 
            being stored.

        Raises
        ------
        ValueError
            If account creation fails due to a database error or any other reason.
        """
        hashed_password = generate_password_hash(password)
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)",
                               (username, hashed_password))
                conn.commit()
                logger.info("Account created for user %s", username)
            except Exception as e:
                logger.error("Failed to create account for user %s: %s", username, e)
                raise ValueError(f"Failed to create account: {e}")

    def login(self, username: str, password: str) -> bool:
        """Verify user credentials and log in.

        This method authenticates a user by verifying the provided password 
        against the hashed password stored in the database for the given username. 
        If the credentials match, the user is logged in successfully.

        Parameters
        ----------
        username : str
            The username of the account to authenticate.
        password : str
            The plaintext password provided for authentication.

        Returns
        -------
        bool
            True if the login is successful (credentials match); otherwise, False.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT hashed_password FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()

        if row and check_password_hash(row[0], password):
            logger.info("User %s logged in successfully", username)
            return True

        logger.error("Login failed for user %s", username)
        return False

    def update_password(self, username: str, new_password: str):
        """Update the user's password.

        This method updates the password for a specified user by hashing the 
        new password and storing it in the database. The change is logged for 
        auditing purposes.

        Parameters
        ----------
        username : str
            The username of the account whose password is to be updated.
        new_password : str
            The new plaintext password to replace the old password. It will be 
            securely hashed before being stored.
        """
        hashed_password = generate_password_hash(new_password)
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET hashed_password = ? WHERE username = ?",
                           (hashed_password, username))
            conn.commit()
            logger.info("Password updated for user %s", username)
