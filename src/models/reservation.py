"""
Module: reservation_model.py
Description: This module defines the Reservation class model used for storing reservation information in a database.

Classes:
    Reservation: A class representing a reservation, containing details such as room, user, guests, dates, cost, and payment.

Usage Example:
    from src.extensions import db
    from reservation_model import Reservation
    from hotel_room_model import HotelRoom  # Importing the HotelRoom model for the relationship
    from user_model import User  # Importing the User model for the relationship
    from payment_model import Payment  # Importing the Payment model for the relationship
    from datetime import datetime
    
    # Create a new reservation instance
    new_reservation = Reservation(room_id=1, user_id=2, num_guests=2, checkin_date='2023-09-01', checkout_date='2023-09-05', total_cost=500.00, reserved_date=datetime.now())

    # Add the reservation to the database session and commit changes
    db.session.add(new_reservation)
    db.session.commit()
"""

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
        payment (Payment): Relationship to the Payment associated with the reservation.

    Usage Example:
        from src.extensions import db
        from reservation_model import Reservation
        from hotel_room_model import HotelRoom
        from user_model import User
        from payment_model import Payment
        from datetime import datetime
        
        # Create a new reservation instance
        new_reservation = Reservation(room_id=1, user_id=2, num_guests=2, 
        checkin_date='09-01-2023', checkout_date='09-05-2023', total_cost=500.00, reserved_date=datetime.now())

        # Add the reservation to the database session and commit changes
        db.session.add(new_reservation)
        db.session.commit()"""
        
    id = db.Column(db.Integer, primary_key=True)
    room = db.relationship('HotelRoom', backref='reservations', lazy=True)
    user = db.relationship('User', backref='reservations', lazy=True)
    num_guests = db.Column(db.Integer, nullable=False)
    checkin_date = db.Column(db.Date, nullable=False)
    checkout_date = db.Column(db.Date, nullable=False)
    reserved_date = db.Column(db.DateTime, default=datetime.now())
    total_cost = db.Column(db.Float, nullable=False)
    payment = db.relationship('Payment', backref='reservation')
