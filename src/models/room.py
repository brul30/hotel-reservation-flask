from src.extensions import db

class RoomType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float)
    description = db.Column(db.String(200))
    max_occupancy = db.Column(db.Integer)
    num_beds = db.Column(db.Integer, nullable=False)
    #rooms = db.relationship('Room', backref='room_type', lazy=True)

#add Room Class alter on
#class Room(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     room_number = db.Column(db.String(10), nullable=False)
#     room_type_id = db.Column(db.Integer, db.ForeignKey('room_type.id'), nullable=False) """


