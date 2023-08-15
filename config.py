"""Module: config.py
Description: This module defines a configuration class containing configuration variables for a Flask application, including database settings and JWT (JSON Web Token) secret key.

Classes:
    Config: A configuration class containing various settings for a Flask application.

Usage Example:
    # Import the Config class into your Flask application
    from config import Config

    # Create a Flask app instance and set the configuration using the Config class
    app = Flask(__name__)
    app.config.from_object(Config)

    # Access configuration variables using the app's config attribute
    secret_key = app.config['SECRET_KEY']
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    jwt_secret_key = app.config['JWT_SECRET_KEY']
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config: 
    """
    Attributes:
        SECRET_KEY (str): Secret key used for securing the application and sessions.
        SQLALCHEMY_DATABASE_URI (str): URI for connecting to the database.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disable Flask-SQLAlchemy modification tracking.
        JWT_SECRET_KEY (str): Secret key used for encoding and decoding JSON Web Tokens (JWT).

    Usage Example:
        # Import the Config class into your Flask application
        from config import Config

        # Create a Flask app instance and set the configuration using the Config class
        app = Flask(__name__)
        app.config.from_object(Config)

        # Access configuration variables using the app's config attribute
        secret_key = app.config['SECRET_KEY']
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        jwt_secret_key = app.config['JWT_SECRET_KEY']"""
    SECRET_KEY=os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
    
