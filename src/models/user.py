from src.extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(80),unique=False,nullable=False)
    last_name = db.Column(db.String(80),unique=False,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password= db.Column(db.Text(),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.now())
    updated_at = db.Column(db.DateTime,onupdate=datetime.now())
    reservations = db.relationship("Reservation",backref="user")
    role = db.Column(db.String(20), nullable=False, default='user')
    def __repr__(self) -> str:
        return 'User>>> {self.first_name} {self.last_name}'
