"""
a) get_routes.py
b) August 2023
c) Miguel Hernandez
d) This module defines a Flask Blueprint named 'get_routes' that handles various GET endpoints related to retrieving room and reservation information.
e) It provides routes for fetching room details, user-specific reservations, and a test endpoint.
Requires JWT authentication.
Returns user's first name and ID in JSON format.
Returns HTTP 200 OK if successful. """
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
    """Test endpoint to check user authentication.

    Returns:
        response (json): A JSON response containing the user's first name and ID.
            - HTTP 200 OK: If the user is authenticated."""
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()

    return jsonify({
        'username': user.username,
        'email' : user.email
    }),HTTP_200_OK


