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
    
    reservation = Reservation.query.filter_by(id=id,user_id=current_user).first()

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

    if 'number_of_guest' in request_data:
        new_number_of_guest = request_data.get('number_of_guest')
        reservation.number_of_guest = new_number_of_guest  

    if 'is_active' in request_data:
        if request_data.get('is_active') == "false" or "False":
            reservation.is_active = False 
                
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
            'reservation_id': reservation.id,
            'reservation_is_active': reservation.is_active,
        }),HTTP_200_OK

