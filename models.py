from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone
import enum

db = SQLAlchemy()

class TicketStatus(enum.Enum):
    RESERVED = 'reserved'  # 预订
    PAID = 'paid'          # 支付
    CANCELED = 'canceled'  # 取消

class TicketType(enum.Enum):
    VIP = 'VIP'
    REGULAR = 'regular'  # 普通票

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # 一个用户可以拥有多张演唱会门票（与 ConcertTicket 的一对多关系）
    concert_tickets = db.relationship('ConcertTicket', backref='user', lazy=True)

class Concert(db.Model):
    __tablename__ = 'concerts'
    id = db.Column(db.Integer, primary_key=True)
    concert_name = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    venue = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    concert_date = db.Column(db.DateTime, nullable=False)
    cover_image_url = db.Column(db.String(500), nullable=True)
    available_tickets = db.Column(db.Integer, nullable=False, default=1000)

    # VIP 和 普通票 价格
    vip_ticket_price = db.Column(db.Float, nullable=False)
    regular_ticket_price = db.Column(db.Float, nullable=False)

    # 一场演唱会可以有多张门票（与 ConcertTicket 的一对多关系）
    concert_tickets = db.relationship('ConcertTicket', backref='concert', lazy=True)

class ConcertTicket(db.Model):
    __tablename__ = 'concert_tickets'
    id = db.Column(db.Integer, primary_key=True)
    concert_id = db.Column(db.Integer, db.ForeignKey('concerts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seat_number = db.Column(db.String(10))
    ticket_type = db.Column(db.Enum(TicketType), nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(TicketStatus), default=TicketStatus.RESERVED, nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(255), nullable=False)
    cinema_name = db.Column(db.String(255), nullable=False)
    hall = db.Column(db.String(100), nullable=False)  # 影厅名称
    show_time = db.Column(db.DateTime, nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)

class MovieTicket(db.Model):
    __tablename__ = 'movie_tickets'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seat_number = db.Column(db.String(10))
    ticket_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # '预订', '支付', '取消'
    purchase_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    movie = db.relationship('Movie', backref='movie_tickets')
    user = db.relationship('User', backref='movie_tickets')

class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(50), nullable=False)
    departure_city = db.Column(db.String(100), nullable=False)
    destination_city = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    airline = db.Column(db.String(100), nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)

class FlightTicket(db.Model):
    __tablename__ = 'flight_tickets'
    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seat_number = db.Column(db.String(10))
    ticket_price = db.Column(db.Float, nullable=False)
    cabin_class = db.Column(db.String(50))  # '经济舱', '商务舱', '头等舱'
    status = db.Column(db.String(20), nullable=False)  # '预订', '支付', '取消'
    purchase_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    flight = db.relationship('Flight', backref='flight_tickets')
    user = db.relationship('User', backref='flight_tickets')