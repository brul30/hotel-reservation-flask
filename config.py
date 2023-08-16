"""
a) Config.py
b) July 2023
c) Miguel Hernandez
d) Gets our application configuration from our .env file. """

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config: 
    """
    Attributes:
        SECRET_KEY (str): Secret key used for securing the application and sessions.
        SQLALCHEMY_DATABASE_URI (str): URI for connecting to the database.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disable Flask-SQLAlchemy modification tracking.
        JWT_SECRET_KEY (str): Secret key used for encoding and decoding JSON Web Tokens (JWT).
    """
    SECRET_KEY=os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
    
