"""
a) delete_routes.py
b) August 2023
c) Miguel Hernandez
d) This blueprint defines routes and functionality for handling various deletion operations related to users,
rooms, and reservations within the application.
e)
    - DELETE /delete/user/<int:user_id>: Deletes a user account.
    - DELETE /delete/room/<int:room_id>: Deletes a room by its ID.
    - DELETE /delete/reservation/<int:reservation_id>: Cancels a reservation by its ID."""
from flask import Blueprint,request,jsonify 
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED , HTTP_401_UNAUTHORIZED,HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_204_NO_CONTENT
from src.extensions import db
from src.models.user import User
from src.models.room import RoomType
from src.models.reservation import Reservation
from flask_jwt_extended import jwt_required,get_jwt_identity

bp = Blueprint('delete_routes',__name__)