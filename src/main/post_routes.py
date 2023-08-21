import datetime
from flask import Blueprint,request,jsonify , current_app
from werkzeug.security import check_password_hash,generate_password_hash
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED , HTTP_401_UNAUTHORIZED,HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.extensions import db
from src.models.user import User
from src.models.reservation import Reservation
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity
import validators
import os
#from flask_mail import Message


bp = Blueprint('post_routes',__name__)

@bp.route('/auth/register',methods=["POST"])
def register():
    try:
        data = request.get_json()

        first_name=data.get('first_name')
        last_name=data.get('last_name')
        email=data.get('email')
        password=data.get('password')
        manager_code = data.get('manager_code')
        role='client'
        static_manager_code = os.getenv("MANGER_KEY")

#        mail = current_app.extensions['mail']
        if manager_code == static_manager_code:
            role = 'manager'
        
        
        if len(password) < 6:
            return jsonify({'error':"password is too short"}),HTTP_400_BAD_REQUEST

        if not validators.email(email):
            return jsonify({'error':"email is not valid"}),HTTP_400_BAD_REQUEST

        if User.query.filter_by(email=email).first() is not None:
            return jsonify({'error':"email is taken"}),HTTP_400_BAD_REQUEST
        
        if User.query.filter_by(email=email).first() is not None:
            return jsonify({'error':"email is taken"}),HTTP_409_CONFLICT
        
        pwd_hash=generate_password_hash(password)

        user=User(first_name=first_name,last_name=last_name,password=pwd_hash,email=email,role=role)
        db.session.add(user)
        db.session.commit()
        access=create_access_token(identity=user.id)

        return jsonify({
            'message': "User Created",
            'first_name':first_name,
            'access_token':access
            }),HTTP_201_CREATED

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

@bp.route('/auth/login',methods=["POST"])
def login():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        user=User.query.filter_by(email=email).first()

        if user:
            is_pass_correct = check_password_hash(user.password,password)
            
            if is_pass_correct:
#                refresh=create_refresh_token(identity=user.id)
                access=create_access_token(identity=user.id)

                return jsonify({
                    'user':{
                       # 'refresh':refresh,
                        'access': access,
                        'first_name':user.first_name,
                        'role':user.role,
                    }
                }),HTTP_200_OK

        return jsonify({'error':"Wrong crdentials"}), HTTP_401_UNAUTHORIZED
    
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR



@bp.route('/auth/token/refresh',methods=["POST"])
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token (identity=identity)

    return jsonify({'access':access}),HTTP_200_OK


@bp.route('/makeReservation',methods=["POST"])
@jwt_required()
def make_reservation():
    try:
        # Get data from the request
        user_id = get_jwt_identity()
        data = request.get_json()

        if not User.query.filter_by(id=user_id).first():
            return jsonify({'error':'User not found'})
        # valid range is from 1-4.

        room_id = data.get('room_id')
        card_number = data.get('card_number')
        number_of_guest = data.get('number_of_guest')
        total_price = data.get('total_price')


        date_of_occupancy = datetime.datetime(
            year=data.get("date_of_occupancy")["year"],
            month=data.get("date_of_occupancy")["month"],
            day=data.get("date_of_occupancy")["day"]
        )
        date_of_departure = datetime.datetime(
            year=data.get("date_of_departure")["year"],
            month=data.get("date_of_departure")["month"],
            day=data.get("date_of_departure")["day"]
        )
        if len(card_number) != 16:
            return jsonify({'error':"Invalid room id"}), HTTP_400_BAD_REQUEST

        if room_id not in {1,2,3}:
            return jsonify({'error':"Invalid room id"}), HTTP_400_BAD_REQUEST

        if number_of_guest not in {1,2,3,4}:
            return jsonify({'error':"Invalid guest range"}), HTTP_400_BAD_REQUEST

        # Create a new reservation
        reservation = Reservation(
            room_id=room_id,
            total_price = total_price,
            user_id=user_id,
            card_number=card_number, 
            date_of_occupancy=date_of_occupancy,
            date_of_departure=date_of_departure,
            number_of_guest=number_of_guest
        )

        # Add the reservation to the database
        db.session.add(reservation)
        db.session.commit()

        return jsonify({'message': 'Reservation successfully created'}), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    


@bp.route('/show/report', methods=['PUT'])
@jwt_required()
def report():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        # Check if the user's role is 'manager'
        data = request.get_json()
        year = data.get('year')
        month = data.get('month')
        reservations = Reservation.query.all()

        cancellation_count = 0
        active_count = 0
        month_total_profit = 0
        user_registered_count = 0

        for reservation in reservations:
            if (reservation.created_at.year == year) and (reservation.created_at.month == month):
                if reservation.is_active:
                    active_count += 1
                    # room_type = RoomType.query.get(reservation.room_id)
                    month_total_profit += reservation.total_price
                else:
                    cancellation_count += 1
                    
        clients = User.query.all()
        for user in clients:
            if (user.created_at.year == year) and (user.created_at.month == month):
                user_registered_count += 1

        reservations_booked = active_count + cancellation_count

        return jsonify({
                "reservations_booked":reservations_booked,
                "cancelled_reservation":cancellation_count,
                "active_reservations":active_count,
                "user_registered":user_registered_count,
                "month_total_profit":month_total_profit
                })
    except Exception as e:
        return jsonify({'error': str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
