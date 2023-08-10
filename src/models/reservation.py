from src.extensions import db
from datetime import datetime

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room = db.relationship('HotelRoom', backref='reservations', lazy=True)
    user = db.relationship('User', backref='reservations', lazy=True)
    num_guests = db.Column(db.Integer, nullable=False)
    checkin_date = db.Column(db.Date, nullable=False)
    checkout_date = db.Column(db.Date, nullable=False)
    reserved_date = db.Column(db.DateTime, default=datetime.now())
    total_cost = db.Column(db.Float, nullable=False)
