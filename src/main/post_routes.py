from flask import Blueprint,request,jsonify 

from werkzeug.security import check_password_hash,generate_password_hash
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED , HTTP_401_UNAUTHORIZED,HTTP_200_OK
import validators
from src.extensions import db
from src.models.user import User
from src.models.room import HotelRoom
from datetime import datetime
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity

bp = Blueprint('post_routes',__name__)

@bp.route('/auth/register',methods=["POST"])
def register():
    
    first_name=request.json['first_name']
    last_name=request.json['last_name']
    email=request.json['email']
    password=request.json['password']
    
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

    return jsonify({
        'message': "User Created",
    }),HTTP_201_CREATED


@bp.route('/auth/login',methods=["POST"])
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    user=User.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.password,password)
        
        if is_pass_correct:
            refresh=create_refresh_token(identity=user.id)
            access=create_access_token(identity=user.id)

            return jsonify({
                'user':user,
                'refresh':refresh,
                'access': access,
            }),HTTP_200_OK
    return jsonify({'error':"Wrong crdentials"}), HTTP_401_UNAUTHORIZED


@bp.route('/auth/token/refresh',methods=["POST"])
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token (identity=identity)

    return jsonify({
        'access':access
    }),HTTP_200_OK

# Accept room_id, checkin_date and checkout_id
# Return true if the room is available for the above dates
@bp.route('/check_availability', methods=['POST'])
def check_room_availability():
    try:
        # Get data from the request JSON
        data = request.get_json()
        room_id = data.get('room_id')
        checkin_date_js = data.get('checkin_date')
        checkout_date_js = data.get('checkout_date')

        # Convert JavaScript Date objects to Python datetime objects
        checkin_date = datetime.strptime(checkin_date_js, '%Y-%m-%dT%H:%M:%S.%fZ')
        checkout_date = datetime.strptime(checkout_date_js, '%Y-%m-%dT%H:%M:%S.%fZ')

        # Fetch the room based on room_id
        room = HotelRoom.query.get(room_id)

        if not room:
            return jsonify({'error': 'Room not found'}), 404

        # Check if the room is available for the specified stay period
        reservations = room.reservations
        for reservation in reservations:
            if checkin_date <= reservation.checkout_date or checkout_date >= reservation.checkin_date:
                return jsonify({'isRoomAvailable': False}), 200

        return jsonify({'isRoomAvailable': True}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400
