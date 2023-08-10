from src.extensions import db

class HotelRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.Integer, unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    num_beds = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.Integer, nullable=False)
