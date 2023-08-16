"""
a) __init__.py
b) July 2023
c) Miguel Hernandez 
d) This File will contain the application factory. 
It's used to initialize the application instance and set up any necessary configurations or extensions.
e) N/A """
#factory function
#everytime we import src __init__.py is automatically imported

# The __init__.py serves double duty: it will contain the application factory, 
# and it tells Python that the HotelBackend directory should be treated as a package.
from flask import Flask,jsonify
from src.extensions import db
from flask_jwt_extended import JWTManager
from config import Config
"""Factory Function for Creating Flask Application

This module contains a factory function `create_app` that is responsible for creating and configuring a Flask application for the HotelBackend project. The application is configured using the provided `Config` class and is set up with necessary extensions and blueprints.

Functions:
    create_app(test_config=Config): 
        This function creates and configures a Flask application instance. It sets up the application's configuration, initializes the database using SQLAlchemy, integrates JWT authentication using Flask-JWT-Extended, and registers a main blueprint from the `src.main` module. The main blueprint likely contains routes and views for the core functionality of the application.

    Parameters:
        test_config (class, optional): 
            An optional configuration class to use when creating the application. The default is the `Config` class provided in the configuration module.

Returns:
    app (Flask):
        The configured Flask application instance ready to be run.

Note:
    - The `__init__.py` file serves as a package initializer and is automatically imported when the `src` module is imported.
    - The `Config` class holds configuration settings for the application.
    - The application factory pattern allows for easier testing and flexibility in configuration changes by creating separate instances of the application.
    - The factory function initializes the database, JWT authentication, and blueprints to structure the application's components.

Example Usage:
    # Creating the Flask application using the default configuration
    from app import create_app
    app = create_app()
    app.run()

    # Creating the Flask application with a custom configuration
    from config import DevelopmentConfig
    app = create_app(test_config=DevelopmentConfig)
    app.run()"""
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
        