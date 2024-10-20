# views/flight.py
from flask import Blueprint, request, jsonify, render_template, current_app, url_for
from flask_login import login_required, current_user
from database import db
from models import Flight, FlightBooking
from sqlalchemy import and_
from datetime import datetime, date

flight_bp = Blueprint('flight', __name__)

# 添加一个机场列表（这里只是示例，你可能需要从数据库中获取真实数据）
AIRPORTS = [
    {'code': 'AKL', 'name': 'Auckland Airport'},
    {'code': 'WLG', 'name': 'Wellington Airport'},
    {'code': 'CHC', 'name': 'Christchurch Airport'},
    {'code': 'ZQN', 'name': 'Queenstown Airport'},
    {'code': 'DUD', 'name': 'Dunedin Airport'},
]

@flight_bp.route('/flights')
def flights():
    is_logged_in = current_user.is_authenticated
    user_email = current_user.email if is_logged_in else ''
    today = date.today().isoformat()  # 获取今天的日期作为日期选择器的最小值
    return render_template('flights.html', airports=AIRPORTS, today=today, 
                           is_logged_in=is_logged_in, user_email=user_email)

@flight_bp.route('/search_flights', methods=['POST'])
def search_flights():
    data = request.get_json()
    departure = data.get('departure')
    arrival = data.get('arrival')
    date = data.get('date')

    # 转换日期字符串为 date 对象
    search_date = datetime.strptime(date, '%Y-%m-%d').date()

    # 查询数据库
    flights = Flight.query.filter(
        and_(
            Flight.departure_airport == departure,
            Flight.arrival_airport == arrival,
            Flight.departure_date == search_date
        )
    ).all()

    # 将查询结果转换为 JSON 格式
    flight_results = []
    for flight in flights:
        flight_results.append({
            'id': flight.id,
            'flight_number': flight.flight_number,
            'airline': flight.airline,
            'departure_time': flight.departure_time.strftime('%H:%M'),
            'arrival_time': flight.arrival_time.strftime('%H:%M'),
            'economy_price': flight.economy_price,
            'business_price': flight.business_price,
            'available_economy_seats': flight.available_economy_seats,
            'available_business_seats': flight.available_business_seats
        })

    return jsonify(flight_results)

@flight_bp.route('/book_flight', methods=['POST'])
@login_required
def book_flight():
    data = request.get_json()
    flight_id = data.get('flight_id')
    seat_type = data.get('seat_type')

    flight = Flight.query.get_or_404(flight_id)
    
    # 检查座位是否还有余票
    if seat_type == 'economy' and flight.available_economy_seats <= 0:
        return jsonify({'success': False, 'message': 'No economy seats available'}), 400
    elif seat_type == 'business' and flight.available_business_seats <= 0:
        return jsonify({'success': False, 'message': 'No business seats available'}), 400

    # 计算票价
    price = flight.economy_price if seat_type == 'economy' else flight.business_price

    # 创新的预订
    new_booking = FlightBooking(
        user_id=current_user.id,
        flight_id=flight_id,
        seat_type=seat_type,
        price=price
    )
    db.session.add(new_booking)

    # 更新可用座位数
    if seat_type == 'economy':
        flight.available_economy_seats -= 1
    else:
        flight.available_business_seats -= 1

    try:
        db.session.commit()
        return jsonify({
            'success': True, 
            'message': 'Flight booked successfully!', 
            'booking_id': new_booking.id,
            'redirect_url': url_for('misc.flight_booking_success', booking_id=new_booking.id)
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error booking flight: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred while booking the flight.'}), 500