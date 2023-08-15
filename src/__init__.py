#factory function
#everytime we import src __init__.py is automatically imported

# The __init__.py serves double duty: it will contain the application factory, 
# and it tells Python that the HotelBackend directory should be treated as a package.
from flask import Flask,jsonify
from src.extensions import db
from flask_jwt_extended import JWTManager
from config import Config
"""This is a factory function that controls everything that happens in the app"""
def create_app(test_config=Config):
    
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    from src.main import bp as main_bp
    
   
    # Initializes the database
    db.app=app # type: ignore
    db.init_app(app)

    JWTManager(app)
    app.register_blueprint(main_bp)
  
    #app.register_blueprint(hotel) 
   

    return app
print(help(create_app))
        