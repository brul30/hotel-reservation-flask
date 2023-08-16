import datetime
from flask import Blueprint,request,jsonify 
from werkzeug.security import check_password_hash,generate_password_hash
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED , HTTP_401_UNAUTHORIZED,HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.extensions import db
from src.models.user import User
from src.models.reservation import Reservation
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity
import validators

bp = Blueprint('post_routes',__name__)

@bp.route('/auth/register',methods=["POST"])
def register():
    try:
        data = request.get_json()

        first_name=data.get('first_name')
        last_name=data.get('last_name')
        email=data.get('email')
        password=data.get('password')
        
        if len(password) < 6:
            return jsonify({'error':"password is too short"}),HTTP_400_BAD_REQUEST

        if not validators.email(email):
            return jsonify({'error':"email is not valid"}),HTTP_400_BAD_REQUEST

        if User.query.filter_by(email=email).first() is not None:
            return jsonify({'error':"email is taken"}),HTTP_400_BAD_REQUEST
        
        if User.query.filter_by(email=email).first() is not None:
            return jsonify({'error':"email is taken"}),HTTP_409_CONFLICT
        
        pwd_hash=generate_password_hash(password)

        user=User(first_name=first_name,last_name=last_name,password=pwd_hash,email=email)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': "User Created",}),HTTP_201_CREATED

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
                refresh=create_refresh_token(identity=user.id)
                access=create_access_token(identity=user.id)

                return jsonify({
                    'user':{
                        'refresh':refresh,
                        'access': access,
                        'first_name':user.first_name,
                        'email':user.email,
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
def make_reservation():
    try:
        # Get data from the request
        data = request.get_json()

        room_id = data.get('room_id')
        user_id = data.get('user_id')
        card_number = data.get('card_number')


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

        if room_id not in {1,2,3}:
            return jsonify({'error':"Invalid room id"}), HTTP_401_UNAUTHORIZED


        # Create a new reservation
        reservation = Reservation(
            room_id=room_id,
            user_id=user_id,
            card_number=card_number,  # Use the ID of the found payment record
            date_of_occupancy=date_of_occupancy,
            date_of_departure=date_of_departure
        )

        # Add the reservation to the database
        db.session.add(reservation)
        db.session.commit()

        return jsonify({'message': 'Reservation successfully created'}), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    



    