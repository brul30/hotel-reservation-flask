from src.extensions import db
from datetime import datetime

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manager = db.relationship('Manager', backref='reports', lazy=True)
    type = db.Column(db.String(50), nullable=False)
    result = db.Column(db.Text, nullable=False)
    generated_date = db.Column(db.DateTime, default=datetime.now())
