from flask import Blueprint
bp = Blueprint('main',__name__,url_prefix="/api/v1")

from src.main.get_routes import bp as get_bp
from src.main.post_routes import bp as post_bp
from src.main.put_routes import bp as put_bp

bp.register_blueprint(get_bp)
bp.register_blueprint(post_bp)
bp.register_blueprint(put_bp)


