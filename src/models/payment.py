from src.extensions import db

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.String(16), unique=True, nullable=False)
    cardholder_name = db.Column(db.String(100), nullable=False)
