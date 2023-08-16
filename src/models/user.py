"""
a) user.py
b) July 2023
c) Miguel Hernandez
d) This module defines the User class model used for storing user information in a database.
e) A class representing a user, including details such as name, email, password, and reservation history."""
from src.extensions import db
from datetime import datetime

class User(db.Model):
    """ Represents a user in the database.

    Attributes:
        id (int): Primary key identifier for the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (str): Email address of the user (must be unique).
        password (str): Password associated with the user's account.
        created_at (datetime): Date and time when the user was created (default is the current date and time).
        updated_at (datetime): Date and time when the user's information was last updated.
        reservations (List[Reservation]): List of reservations associated with the user. """
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(80),unique=False,nullable=False)
    last_name = db.Column(db.String(80),unique=False,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password= db.Column(db.Text(),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.now())
    updated_at = db.Column(db.DateTime,onupdate=datetime.now())
    payment = db.relationship('Payment', backref='user', lazy=True)

    def __repr__(self) -> str:
        return 'User>>> {self.first_name} {self.last_name}'