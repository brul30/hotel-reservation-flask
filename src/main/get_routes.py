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
        reservations = Reservation.query.all()

        # reservations_booked = Reservation.query.filter(
        #     extract('year', Reservation.created_at) == year,
        #     extract('month', Reservation.created_at) == month
        #     ).count()

        # cancellation_count = Reservation.query.filter(
        #     extract('year', Reservation.created_at) == year,
        #     extract('month', Reservation.created_at) == month,
        #     Reservation.is_active == False  
        #     ).count()


        # user_registered = User.query.filter(
        #     extract('year', User.created_at) == year,
        #     extract('month', User.created_at) == month
        #     ).count()
        
        # reservations = Reservation.query.filter(
        #     extract('year', Reservation.created_at) == year,
        #     extract('month', Reservation.created_at) == month,
        #     Reservation.is_active == True  
        #     ).all()
        
        # month_total_profit = 0

        # for reservation in reservations:
        #     room_type = RoomType.query.get(reservation.room_id)
        #     month_total_profit += room_type.price
        
        # active_count = reservations_booked-cancellation_count

        cancellation_count = 0
        user_registered = 0
        active_count = 0
        month_total_profit = 0

        for reservation in reservations:
            if (reservation.created_at.year == year) and (reservation.created_at.month == month):
                if reservation.is_active:
                  active_count += 1
                  room_type = RoomType.query.get(reservation.room_id)
                  month_total_profit += room_type.price
                else:
                  cancellation_count += 1

        for user in user_registered:
            if (user.created_at.year == year) and (user.created_at.month == month):
                user_registered_count += 1

        reservations_booked = active_count + cancellation_count

        return jsonify({
            "reservations_booked":reservations_booked,
            "cancelled_reservation":cancellation_count,
            "active_reservations":active_count,
            "user_registered":user_registered,
            "month_total_profit":month_total_profit
            })
    else:
        return jsonify({"message": "Unauthorized for manager role"}), HTTP_403_FORBIDDEN
