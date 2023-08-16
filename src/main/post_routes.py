"""
a) post_routes.py
b) August 2023
c) Miguel Hernandez 
d) This module defines a Flask Blueprint named 'post_routes' 
that handles various POST endpoints related to user registration, login, token refresh, and reservation creation."""

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

