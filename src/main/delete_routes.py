"""delete_routes.py - Blueprint for handling deletion-related routes in a Flask web application.

This blueprint defines routes and functionality for handling various deletion operations related to users,
rooms, and reservations within the application.

Routes:
    - DELETE /delete/user/<int:user_id>: Deletes a user account.
    - DELETE /delete/room/<int:room_id>: Deletes a room by its ID.
    - DELETE /delete/reservation/<int:reservation_id>: Cancels a reservation by its ID.

Required Modules and Libraries:
    - Flask: A micro web framework for Python.
    - src.constants.http_status_codes: Module containing HTTP status code constants.
    - src.extensions.db: The database extension instance (presumably SQLAlchemy).
    - src.models.user: Module defining the User model for user-related operations.
    - src.models.room: Module defining the RoomType model for room-related operations.
    - src.models.reservation: Module defining the Reservation model for reservation-related operations.
    - Flask-JWT-Extended: Extension for adding JWT (JSON Web Token) support to Flask applications.

Blueprint Usage:
    This blueprint sets up routes that handle different deletion operations in the application.
    It includes routes for deleting user accounts, rooms, and reservations. These routes are protected
    using JWT authentication, ensuring that only authenticated users can access them.

    To use this blueprint in your Flask application, you can register it like this:
    ```python
    from flask import Flask
    from .delete_routes import bp as delete_bp

    app = Flask(__name__)
    app.register_blueprint(delete_bp)
    ```

Note:
    - This docstring provides an overview of the functionality encapsulated in the 'delete_routes' blueprint.
      Further details about specific route implementations and function logic can be found within the
      corresponding routes defined in this blueprint."""
from flask import Blueprint,request,jsonify 
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED , HTTP_401_UNAUTHORIZED,HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_204_NO_CONTENT
from src.extensions import db
from src.models.user import User
from src.models.room import RoomType
from src.models.reservation import Reservation
from flask_jwt_extended import jwt_required,get_jwt_identity

bp = Blueprint('delete_routes',__name__)