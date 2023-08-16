"""
a) Reservation.py
b) July 2023
c) Miguel Hernandez & Shawn Takhirov
d)  This module defines the Reservation class model used for storing reservation information in a database.
e) A class representing a reservation, containing details such as room, user, guests, dates, cost, and payment. """

from src.extensions import db
from datetime import datetime

class Reservation(db.Model):
    """ Represents a reservation in the database.

    Attributes:
        id (int): Primary key identifier for the reservation.
        room_id (int): Foreign key reference to the associated HotelRoom.
        room (HotelRoom): Relationship to the HotelRoom associated with the reservation.
        user_id (int): Foreign key reference to the associated User.
        user (User): Relationship to the User who made the reservation.
        num_guests (int): Number of guests included in the reservation.
        checkin_date (datetime.date): Date of check-in for the reservation.
        checkout_date (datetime.date): Date of check-out for the reservation.
        reserved_date (datetime.datetime): Date and time when the reservation was made (default is the current date and time).
        total_cost (float): Total cost of the reservation.
        payment (Payment): Relationship to the Payment associated with the reservation. """

        
    id = db.Column(db.Integer, primary_key=True)
    room = db.relationship('HotelRoom', backref='reservations', lazy=True)
    user = db.relationship('User', backref='reservations', lazy=True)
    num_guests = db.Column(db.Integer, nullable=False)
    checkin_date = db.Column(db.Date, nullable=False)
    checkout_date = db.Column(db.Date, nullable=False)
    reserved_date = db.Column(db.DateTime, default=datetime.now())
    total_cost = db.Column(db.Float, nullable=False)
    payment = db.relationship('Payment', backref='reservation')
