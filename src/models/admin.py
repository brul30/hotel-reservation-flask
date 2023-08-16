"""
a) admin.py
b) July 2023
c) Miguel Hernandez
d) This module defines the Manager class model used for representing managers in a database.
e) A class representing a manager, with attributes such as id, first name, last name, email, and password. """
from src.extensions import db
# We use models to definte and create classes
class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
