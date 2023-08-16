"""
a) main.blueprint.py
b) August 2023
c) Miguel Hernandez & Shawn Takhirov
d) This module demonstrates the use of Flask Blueprints to organize and structure routes within a Flask application. """

from flask import Blueprint

bp = Blueprint('main',__name__,url_prefix="/api/v1")

from src.main.get_routes import bp as get_bp
from src.main.post_routes import bp as post_bp

bp.register_blueprint(get_bp)
bp.register_blueprint(post_bp)

