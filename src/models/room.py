from src.extensions import db

class RoomType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    room_number = db.Column(db.Integer)
    price = db.Column(db.Float)
    description = db.Column(db.String(200))
    max_occupancy = db.Column(db.Integer)
    num_beds = db.Column(db.Integer, nullable=False)
    reservations = db.relationship("Reservation",backref="room_type")
