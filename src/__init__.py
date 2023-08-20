#factory function
#everytime we import src __init__.py is automatically imported

# The __init__.py serves double duty: it will contain the application factory, 
# and it tells Python that the HotelBackend directory should be treated as a package.
from flask import Flask,jsonify
from src.extensions import db
from flask_jwt_extended import JWTManager
from config import Config
from src.constants.http_status_codes import HTTP_404_NOT_FOUND,HTTP_500_INTERNAL_SERVER_ERROR
from flask_cors import CORS

def create_app(test_config=Config):
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config) 
    CORS(app)

    from src.main import bp as main_bp
    
   
    
    db.app=app # type: ignore
    db.init_app(app)

    JWTManager(app)
    app.register_blueprint(main_bp)
  
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, Server working on it'}), HTTP_500_INTERNAL_SERVER_ERROR


    return app
        