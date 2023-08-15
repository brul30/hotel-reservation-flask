"""
get_routes Blueprint

This module defines a Flask Blueprint named 'get_routes' that handles various GET endpoints related to retrieving room and reservation information. It provides routes for fetching room details, user-specific reservations, and a test endpoint.

Endpoints:
1. GET /auth/userHomePage: A test endpoint to check user authentication.
    - Requires JWT authentication.
    - Returns user's first name and ID in JSON format.
    - Returns HTTP 200 OK if successful.

2. GET /allRooms: Fetches details of all room types.
    - Returns a list of room dictionaries in JSON format.
    - Returns HTTP 200 OK if successful.
    - Returns HTTP 500 Internal Server Error if there is a server-side issue.

3. GET /userRooms: Fetches reservations made by the authenticated user.
    - Requires JWT authentication.
    - Returns a list of reservation dictionaries in JSON format.
    - Returns HTTP 200 OK if successful.

Dependencies:
- Flask: A micro web framework for Python.
- Flask-JWT-Extended: An extension for Flask that adds JWT support.
- src.models.user.User: A User model class representing users in the system.
- src.models.room.RoomType: A RoomType model class representing different types of rooms.
- src.constants.http_status_codes: A module containing constants for HTTP status codes.
- src.extensions.db: A database extension for SQLAlchemy.
- src.models.reservation.Reservation: A Reservation model class representing reservations.

Attributes:
- bp: A Blueprint instance for creating the 'get_routes' Blueprint.

"""
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


