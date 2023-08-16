"""
a) put_routes.py
b) August 2023
c) Miguel Hernandez
d) This blueprint defines a route and functionality for updating reservation details for a user in the application."""
"""
Routes:
    - PUT /update/userReservation/<int:id>: Updates reservation details for the authenticated user.

Required Modules and Libraries:
    - Flask: A micro web framework for Python.
    - src.constants.http_status_codes: Module containing HTTP status code constants.
    - src.extensions.db: The database extension instance (presumably SQLAlchemy).
    - src.models.user: Module defining the User model for user-related operations.
    - src.models.room: Module defining the RoomType model for room-related operations.
    - src.models.reservation: Module defining the Reservation model for reservation-related operations.
    - Flask-JWT-Extended: Extension for adding JWT (JSON Web Token) support to Flask applications.

Blueprint Usage:
    This blueprint sets up a route that allows an authenticated user to update their reservation details.
    The route supports updating the room ID, date of occupancy, and date of departure for the reservation.

    To use this blueprint in your Flask application, you can register it like this:
    ```python
    from flask import Flask
    from .put_routes import bp as put_bp

    app = Flask(__name__)
    app.register_blueprint(put_bp)
    ```

Note:
    - This docstring provides an overview of the functionality encapsulated in the 'put_routes' blueprint.
      Further details about the route implementation and function logic can be found within the corresponding
      route definition in this blueprint."""
from flask import Blueprint,request,jsonify 
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED , HTTP_401_UNAUTHORIZED,HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_204_NO_CONTENT
from src.extensions import db
from src.models.user import User
from src.models.room import RoomType
from src.models.reservation import Reservation
from flask_jwt_extended import jwt_required,get_jwt_identity

bp = Blueprint('put_routes',__name__)

@bp.route('/update/userReservation/<int:id>', methods=['PUT'])
@jwt_required()
def change_reservation(id):

    
    current_user = get_jwt_identity()

    request_data = request.get_json()
    
    reservation = Reservation.query.filter_by(user_id=current_user,id=id).first()

    if not reservation:
        return jsonify({'error':'reservation not found'}),HTTP_204_NO_CONTENT
    
    if 'room_id' in request_data:
        room_type_id = request_data.get('room_id')
        reservation.room_id = room_type_id

    if 'date_of_occupancy' in request_data:
        new_date_of_occupancy = request_data.get('date_of_occupancy')
        reservation.date_of_occupancy = new_date_of_occupancy

    if 'date_of_departure' in request_data:
        new_date_of_departure = request_data.get('date_of_departure')
        reservation.date_of_departure = new_date_of_departure    
                
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'failed to update reservation', 'details': str(e)}),        

    roomtype = RoomType.query.get(reservation.room_id)
    return jsonify({
            'room_details': {
                'id': roomtype.id,
                'name': roomtype.name,
                'room_number': roomtype.room_number,
                'price': roomtype.price,
                'description': roomtype.description,
                'max_occupancy': roomtype.max_occupancy,
                'num_beds': roomtype.num_beds
            },
            'date_of_occupancy': reservation.date_of_occupancy,
            'date_of_departure': reservation.date_of_departure,
            'reservation_id': reservation.id
        }),HTTP_200_OK