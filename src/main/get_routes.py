from flask import Blueprint,jsonify
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity
from src.models.user import User
from src.constants.http_status_codes import HTTP_200_OK
bp = Blueprint('get_routes',__name__,)

@bp.route("/hotel/me",methods=["GET"])
def me():
    return "me"


@bp.route("/auth/userHomePage",methods=["GET"])
@jwt_required()
def check():
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()

    return jsonify({
        'username': user.username,
        'email' : user.email
    }),HTTP_200_OK


