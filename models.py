# models.py

from flask_login import UserMixin
from database import db
from datetime import datetime

# User 模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

# Event 模型
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    image_url = db.Column(db.String(200))
    details = db.Column(db.Text)

    def __repr__(self):
        return f'<Event {self.title}>'

# EventBooking 模型
class EventBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('event_bookings', lazy=True))
    event = db.relationship('Event', backref=db.backref('bookings', lazy=True))

# Flight 模型
class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(10), nullable=False)
    departure_airport = db.Column(db.String(3), nullable=False)
    arrival_airport = db.Column(db.String(3), nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    departure_time = db.Column(db.Time, nullable=False)
    arrival_date = db.Column(db.Date, nullable=False)
    arrival_time = db.Column(db.Time, nullable=False)
    airline = db.Column(db.String(50), nullable=False)
    economy_price = db.Column(db.Float, nullable=False)
    business_price = db.Column(db.Float, nullable=False)
    available_economy_seats = db.Column(db.Integer, nullable=False)
    available_business_seats = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Flight {self.flight_number}>'

# FlightBooking 模型
class FlightBooking(db.Model):
    __tablename__ = 'flight_bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    seat_type = db.Column(db.String(20), nullable=False)  # 'economy' 或 'business'
    seat_number = db.Column(db.String(10))
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='confirmed', nullable=False)  # 'confirmed', 'cancelled', 'completed'
    payment_status = db.Column(db.String(20), default='pending', nullable=False)  # 'pending', 'paid', 'refunded'

    user = db.relationship('User', backref=db.backref('flight_bookings', lazy=True))
    flight = db.relationship('Flight', backref=db.backref('bookings', lazy=True))

    def __repr__(self):
        return f'<FlightBooking {self.id}: User {self.user_id}, Flight {self.flight_id}>'