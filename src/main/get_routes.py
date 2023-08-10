from flask import Blueprint,jsonify
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity
from src.models.user import User
from src.models.room import HotelRoom
from src.constants.http_status_codes import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
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
        'user': user,
    }),HTTP_200_OK


@bp.route('/rooms', methods=['GET'])
def get_all_rooms():
    try:
        # Fetch all rooms from the database
        rooms = HotelRoom.query.all()

        # Convert the list of room objects to a list of dictionaries
        rooms_data = [
            {
                'id': room.id,
                'room_number': room.room_number,
                'capacity': room.capacity,
                'price': room.price,
                'room_type': room.room_type,
                'num_beds': room.num_beds,
                'floor': room.floor
            }
            for room in rooms
        ]

        return jsonify({'rooms': rooms_data}),HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}),HTTP_500_INTERNAL_SERVER_ERROR

