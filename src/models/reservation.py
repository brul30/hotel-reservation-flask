from src.extensions import db
from datetime import datetime
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room_type.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #card_id = db.Column(db.Integer, db.ForeignKey('payment.id'), nullable=False)
    card_number = db.Column(db.String(16), nullable=False)
    date_of_occupancy = db.Column(db.String(16), nullable=False)
    date_of_departure = db.Column(db.String(16), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
