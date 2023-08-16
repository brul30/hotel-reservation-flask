"""
a) Extensions.py
b) July 2023
c) Miguel Hernandez
d) This file is used to define any extensions. 
e) In this case we are defining the SQLAlchemy library here. """

# This is used for setting up the SQLAlchemy database 
# SQLAlchemy is a database toolkit and object-relational mapper for the Python programming language.
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

