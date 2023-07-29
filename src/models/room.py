from src.extensions import db
from datetime import datetime

class HotelRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.Integer, unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    is_vacant = db.Column(db.Boolean, default=True)
    reservations = db.relationship('Reservation', backref='room', lazy=True)
