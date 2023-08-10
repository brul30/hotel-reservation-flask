from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
db = SQLAlchemy(app)

# Define Reservation model
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.String, nullable=False)
    guest_name = db.Column(db.String, nullable=False)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)

# Endpoint to handle POST request for room reservations
@app.route('/api/reservations', methods=['POST'])
def create_reservation():
    try:
        data = request.json
        room_id = data.get('room_id')
        guest_name = data.get('guest_name')
        check_in = data.get('check_in')
        check_out = data.get('check_out')

        # Basic validation
        if not (room_id and guest_name and check_in and check_out):
            return jsonify({'error': 'All fields are required.'}), 400

        # Fetch room details from the database
        existing_reservation = Reservation.query.filter(
            Reservation.room_id == room_id,
            (Reservation.check_in < check_out) & (Reservation.check_out > check_in)
        ).first()

        if existing_reservation:
            return jsonify({'error': 'Room is not available for selected dates.'}), 400

        # Create a new reservation object
        new_reservation = Reservation(
            room_id=room_id,
            guest_name=guest_name,
            check_in=check_in,
            check_out=check_out
        )

        # Save the reservation to the database
        db.session.add(new_reservation)
        db.session.commit()

        return jsonify({'message': 'Reservation successfully created.'}), 201

    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred while processing the reservation.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
