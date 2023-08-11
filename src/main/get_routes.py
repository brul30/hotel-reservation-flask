from flask import Blueprint,jsonify
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity
from src.models.user import User
from src.models.room import RoomType
from src.constants.http_status_codes import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
bp = Blueprint('get_routes',__name__,)
from src.extensions import db


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
    # Create room type instances 
        if not RoomType.query.all():
            room_type1 = RoomType(name='Standard',room_number=101,price=150,description='Basic room with essential amenities', max_occupancy=2,num_beds=1)
            room_type2 = RoomType( name='Deluxe',room_number=201,price=150,description='Larger room with additional amenities', max_occupancy=3, num_beds=2)
            room_type3 = RoomType( name='Suite',room_number=301,price=150,description='Luxurious suite with a separate living area', max_occupancy=4,num_beds=4)
            db.session.add(room_type1)
            db.session.add(room_type2)
            db.session.add(room_type3)
            db.session.commit()
        # Fetch all rooms from the database
        rooms = RoomType.query.all()

        # Convert the list of room objects to a list of dictionaries
        rooms_data = [
            {
                'id': room.id,
                'name': room.name,
                'room_number': room.room_number,
                'price': room.price,
                'description': room.description,
                'max_occupancy': room.max_occupancy,
                'num_beds': room.num_beds
            }
            for room in rooms
        ]

        return jsonify({'rooms': rooms_data}),HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
