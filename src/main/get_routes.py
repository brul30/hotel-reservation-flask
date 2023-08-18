from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from src.models.user import User
from src.models.room import RoomType
from src.constants.http_status_codes import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_403_FORBIDDEN
from src.extensions import db
from src.models.reservation import Reservation
from sqlalchemy import extract
bp = Blueprint('get_routes',__name__,)

# ``` 
# This endpoint is not doing anything, I made it to rest jwt_required
# I will deleted in due time, DO NOT DELETE 
# ````
@bp.route("/auth/userHomePage",methods=["GET"])
@jwt_required()
def check():
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()

    return jsonify({
        'first_name' : user.first_name,
        'id':user.id
    }),HTTP_200_OK



@bp.route('/show/allRooms', methods=['GET'])
def get_all_rooms():
    try:
    # Create room type instances 
        if not RoomType.query.all():
            room_type1 = RoomType(name='Standard',room_number=101,price=150,description='Basic room with essential amenities', max_occupancy=2,num_beds=1)
            room_type2 = RoomType( name='Deluxe',room_number=201,price=250,description='Larger room with additional amenities', max_occupancy=3, num_beds=2)
            room_type3 = RoomType( name='Suite',room_number=301,price=350,description='Luxurious suite with a separate living area', max_occupancy=4,num_beds=4)
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


@bp.route('/show/userRooms', methods=['GET'])
@jwt_required()
def get_user_rooms():
    user_id = get_jwt_identity()
    reservations = Reservation.query.filter_by(user_id=user_id).all()

    reservation_list = []

    for reservation in reservations:
        roomtype = RoomType.query.get(reservation.room_id)
        reservation_data = {
            'room_details': {
                'room_id': roomtype.id,
                'name': roomtype.name,
                'room_number': roomtype.room_number,
                'price': roomtype.price,
                'description': roomtype.description,
                'max_occupancy': roomtype.max_occupancy,
                'num_beds': roomtype.num_beds
            },
            'date_of_occupancy': reservation.date_of_occupancy,
            'date_of_departure': reservation.date_of_departure,
            'number_of_guest': reservation.number_of_guest,
            'is_active':reservation.is_active,
            'reservatio_id': reservation.id
        }
        reservation_list.append(reservation_data)
        if not reservation_list:
            return jsonify({
            "message":'No reservations made'
        })
    
    # Return the list of reservations as JSON
    return jsonify({'reservations': reservation_list})

@bp.route('/show/report', methods=['GET'])
@jwt_required()
def report():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Check if the user's role is 'manager'
    if user.role == 'manager':

        data = request.get_json()
        year = data.get('year')
        month = data.get('month')

        reservations_booked = Reservation.query.filter(
            extract('year', Reservation.created_at) == year,
            extract('month', Reservation.created_at) == month
            ).count()

        cancellation_count = Reservation.query.filter(
            extract('year', Reservation.created_at) == year,
            extract('month', Reservation.created_at) == month,
            Reservation.is_active == False  
            ).count()


        user_registered = User.query.filter(
            extract('year', User.created_at) == year,
            extract('month', User.created_at) == month
            ).count()
        
        reservations = Reservation.query.filter(
            extract('year', Reservation.created_at) == year,
            extract('month', Reservation.created_at) == month,
            Reservation.is_active == True  
            ).all()
        
        month_total_profit = 0

        for reservation in reservations:
            room_type = RoomType.query.get(reservation.room_id)
            month_total_profit += room_type.price


        active_count = reservations_booked-cancellation_count


        return jsonify({
            "reservations_booked":reservations_booked,
            "cancelled_reservation":cancellation_count,
            "active_reservations":active_count,
            "user_registered":user_registered,
            "month_total_profit":month_total_profit
            })
    else:
        return jsonify({"message": "Unauthorized for manager role"}), HTTP_403_FORBIDDEN