from src.extensions import db
from datetime import datetime
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room_type.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    card_number = db.Column(db.String(16), nullable=False)
    date_of_occupancy = db.Column(db.DateTime, nullable=False)
    date_of_departure = db.Column(db.DateTime, nullable=False)
    number_of_guest = db.Column(db.Integer, nullable=False)
    is_active=db.Column(db.Boolean,default=True)
    total_price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
