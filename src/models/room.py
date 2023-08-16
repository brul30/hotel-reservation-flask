"""
a) room.py
b) July 2023
c) Miguel Hernandez
d) This module defines the HotelRoom class model used for storing hotel room information in a database."""
"""
Classes:
    HotelRoom: A class representing a hotel room, including details such as room number, capacity, status, price, and more.

Usage Example:
    from src.extensions import db
    from hotel_room_model import HotelRoom
    
    # Create a new hotel room instance
    new_room = HotelRoom(room_number=101, capacity=2, is_vacant=True, price=150.00, room_type="Standard", num_beds=1, floor=1)

    # Add the room to the database session and commit changes
    db.session.add(new_room)
    db.session.commit()
"""

from src.extensions import db
"""Represents a hotel room in the database.

    Attributes:
        id (int): Primary key identifier for the hotel room.
        room_number (int): Unique room number for the hotel room.
        capacity (int): Maximum number of guests the room can accommodate.
        is_vacant (bool): Indicates if the room is vacant (default is True).
        price (float): Price of the room per night.
        room_type (str): Type or category of the room.
        num_beds (int): Number of beds in the room.
        floor (int): Floor number where the room is located.

    Usage Example:
        from src.extensions import db
        from hotel_room_model import HotelRoom
        
        # Create a new hotel room instance
        new_room = HotelRoom(room_number=101, capacity=2, is_vacant=True, price=150.00, room_type="Standard", num_beds=1, floor=1)

        # Add the room to the database session and commit changes
        db.session.add(new_room)
        db.session.commit()"""

class HotelRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.Integer, unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    is_vacant = db.Column(db.Boolean, default=True)
    price = db.Column(db.Float, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    num_beds = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.Integer, nullable=False)
