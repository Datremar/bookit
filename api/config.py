import os
import secrets
from datetime import datetime, timedelta
import mysql.connector

# Each Flask web application contains a secret key which used to sign session
# cookies for protection against cookie data tampering.
SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode, that will refresh the page when you make changes.
DEBUG = os.getenv('DEBUG', "True")

# Connect to the MYSQL database
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PASS = os.getenv('MYSQL_ROOT_PASSWORD', '')
MYSQL_NAME = os.getenv('MYSQL_DATABASE', 'bookings')

__CONNECTION = None
def get_db():
    # pylint: disable=global-statement
    global __CONNECTION

    if __CONNECTION:
        return __CONNECTION

    __CONNECTION = mysql.connector.connect(
        host=MYSQL_HOST,
        database=MYSQL_NAME,
        user='root',
        password=MYSQL_PASS
    )
    return __CONNECTION

def get_db_cursor():
    # pylint: disable=global-statement
    global __CONNECTION
    cursor = get_db().cursor()
    if cursor is None:
        __CONNECTION = None
        raise Exception("Cursor is not set")
    return cursor

def close_db_con() -> None:
    # pylint: disable=global-statement
    global __CONNECTION
    if __CONNECTION.is_connected():
        __CONNECTION.close()

    __CONNECTION = None

def generate_token() -> str:
    return secrets.token_urlsafe(16)

def generate_date_delta(token_delta = 12) -> datetime:
    return datetime.now() + timedelta(days=token_delta)
