"""
a) post_routes.py
b) August 2023
c) Miguel Hernandez 
d) This module defines a Flask Blueprint named 'post_routes' 
that handles various POST endpoints related to user registration, login, token refresh, and reservation creation."""

""""
Endpoints:
1. POST /auth/register: Registers a new user.
    - Accepts user registration data in JSON format.
    - Returns HTTP 201 Created if successful.
    - Returns HTTP 400 Bad Request for invalid input data.
    - Returns HTTP 409 Conflict if the email is already taken.
    - Returns HTTP 500 Internal Server Error for server-side issues.

2. POST /auth/login: Logs in a user and provides access and refresh tokens.
    - Accepts user login credentials in JSON format.
    - Returns a JSON response containing access and refresh tokens, user details.
    - Returns HTTP 200 OK if successful.
    - Returns HTTP 401 Unauthorized for incorrect credentials.
    - Returns HTTP 500 Internal Server Error for server-side issues.

3. POST /auth/token/refresh: Refreshes an access token.
    - Requires a valid refresh token in the Authorization header.
    - Returns a JSON response containing a new access token.
    - Returns HTTP 200 OK if successful.

4. POST /makeReservation: Creates a new reservation.
    - Accepts reservation data in JSON format.
    - Returns a JSON response indicating the success of the reservation creation.
    - Returns HTTP 200 OK if successful.
    - Returns HTTP 401 Unauthorized for invalid room IDs.
    - Returns HTTP 500 Internal Server Error for server-side issues.

Dependencies:
- Flask: A micro web framework for Python.
- Flask-JWT-Extended: An extension for Flask that adds JWT support.
- werkzeug.security: Utilities for hashing passwords.
- src.constants.http_status_codes: A module containing constants for HTTP status codes.
- src.extensions.db: A database extension for SQLAlchemy.
- src.models.user.User: A User model class representing users in the system.
- src.models.reservation.Reservation: A Reservation model class representing reservations.

Attributes:
- bp: A Blueprint instance for creating the 'post_routes' Blueprint.

"""
from flask import Blueprint,request,jsonify 

from werkzeug.security import check_password_hash,generate_password_hash
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED , HTTP_401_UNAUTHORIZED,HTTP_200_OK
import validators
from src.extensions import db
from src.models.user import User
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity

bp = Blueprint('post_routes',__name__)

@bp.route('/auth/register',methods=["POST"])
def register():
    
    username=request.json['username']
    email=request.json['email']
    password=request.json['password']
    
    if len(password) < 6:
        return jsonify({'error':"password is too short"}),HTTP_400_BAD_REQUEST
    
    if len(username) < 6:
        return jsonify({'error':"User is too short"}),HTTP_400_BAD_REQUEST
    
    if not username.isalnum() or " " in username:
        return jsonify({'error':"username should be alphanumeric and not include any spaces"}),HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error':"email is not valid"}),HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error':"email is taken"}),HTTP_400_BAD_REQUEST
    
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error':"email is taken"}),HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error':"username is taken"}),HTTP_409_CONFLICT
    
    pwd_hash=generate_password_hash(password)

    user=User(username=username,password=pwd_hash,email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User Created",
        'user': {
            'username': username,
            'email':email,
        }
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
                'user':{
                    'refresh':refresh,
                    'access': access,
                    'username':user.username,
                    'email':user.email,
                }
            }),HTTP_200_OK
    return jsonify({'error':"Wrong crdentials"}), HTTP_401_UNAUTHORIZED


@bp.route('/auth/token/refresh',methods=["POST"])
@jwt_required(refresh=True)
def refresh_users_token():
    """Refresh an access token.

    Returns:
        response (json): A JSON response containing a new access token.
            - HTTP 200 OK: If the token is successfully refreshed."""
    identity = get_jwt_identity()
    access = create_access_token (identity=identity)

    return jsonify({
        'access':access
    }),HTTP_200_OK

