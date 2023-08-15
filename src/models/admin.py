from src.extensions import db
# We use models to definte and create classes
class Manager(db.Model):
    """Module: manager_model.py
Description: This module defines the Manager class model used for representing managers in a database.

Classes:
    Manager: A class representing a manager, with attributes such as id, first name, last name, email, and password.

Usage Example:
    from src.extensions import db
    from manager_model import Manager
    
    # Create a new manager instance
    new_manager = Manager(first_name="Admin", last_name="Manager", email="admin@example.com", password="secretpass")

    # Add the manager to the database session and commit changes
    db.session.add(new_manager)
    db.session.commit()
"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
