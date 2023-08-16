"""
a) main.blueprint.py
b) August 2023
c) Miguel Hernandez 
d) This module demonstrates the use of Flask Blueprints to organize and structure routes within a Flask application. """
"""
Usage Example:
1. Create a new Flask application:

   from flask import Flask
   app = Flask(__name__)

2. Import and create the main Blueprint instance:

   from flask import Blueprint
   bp = Blueprint('main', __name__, url_prefix="/api/v1")

3. Import and register sub-Blueprints (get_routes and post_routes):

   from src.main.get_routes import bp as get_bp
   from src.main.post_routes import bp as post_bp

   bp.register_blueprint(get_bp)
   bp.register_blueprint(post_bp)
   4. Register the main Blueprint with the Flask application:

   app.register_blueprint(bp)

5. Run the Flask application:

   if __name__ == "__main__":
       app.run()
       Purpose of Using Blueprints:
- Flask Blueprints help modularize and organize your application's routes and views.
- They encourage good design practices by allowing you to create reusable components.
- Blueprint URLs are automatically prefixed with the specified URL prefix, enhancing route organization."""

from flask import Blueprint

bp = Blueprint('main',__name__,url_prefix="/api/v1")

from src.main.get_routes import bp as get_bp
from src.main.post_routes import bp as post_bp

bp.register_blueprint(get_bp)
bp.register_blueprint(post_bp)

