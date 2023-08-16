"""
a) __init__.py
b) July 2023
c) Miguel Hernandez 
d) This File will contain the application factory. 
It's used to initialize the application instance and set up any necessary configurations or extensions. 
e) Serves as a factory function, every time we import src __init__.py is automatically imported
The __init__.py serves double duty: it will contain the application factory, 
and it tells Python that the HotelBackend directory should be treated as a package. """
#factory function
#everytime we import src __init__.py is automatically imported

# The __init__.py serves double duty: it will contain the application factory, 
# and it tells Python that the HotelBackend directory should be treated as a package"
from flask import Flask,jsonify
from src.extensions import db
from flask_jwt_extended import JWTManager
from config import Config
"""Factory Function for Creating Flask Application
This module contains a factory function `create_app` that is responsible for creating and configuring a Flask application for the HotelBackend project. 
The application is configured using the provided `Config` class and is set up with necessary extensions and blueprints.
    create_app(test_config=Config): 
        This function creates and configures a Flask application instance. 
        It sets up the application's configuration, initializes the database using SQLAlchemy, integrates JWT authentication using Flask-JWT-Extended, and registers a main blueprint from the `src.main` module."""
def create_app(test_config=Config):
    
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    from src.main import bp as main_bp
    
   
    # Initializes the database
    db.app=app # type: ignore
    db.init_app(app)

    JWTManager(app)
    app.register_blueprint(main_bp)
  
    #app.register_blueprint(hotel)""
   

    return app
        