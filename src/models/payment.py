# from src.extensions import db
# from src.models.user import User
# class Payment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     card_number = db.Column(db.String(16), unique=True, nullable=False)
#     cardholder_name = db.Column(db.String(100), nullable=False)
    
#     user = db.relationship("User", back_populates="Payment")
