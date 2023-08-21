from datetime import timedelta
import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    load_dotenv()
    SECRET_KEY=os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES= timedelta(days=1)  # Set access token expiration to 1 day
