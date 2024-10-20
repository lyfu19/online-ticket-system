# views/misc.py
from flask import Blueprint, session, redirect, request, url_for, current_app, render_template, abort, jsonify
from flask_login import current_user, login_required
from models import EventBooking, FlightBooking

misc_bp = Blueprint('misc', __name__)

@misc_bp.route('/set_language/<lang>')
def set_language(lang):
    if lang not in current_app.config['BABEL_SUPPORTED_LOCALES']:
        lang = current_app.config['BABEL_DEFAULT_LOCALE']  # 默认语言
    session['lang'] = lang
    return redirect(request.referrer or url_for('misc.index'))

@misc_bp.route('/maori-culture')
def maori_culture():
    is_logged_in = current_user.is_authenticated
    user_email = current_user.email if is_logged_in else ''
    return render_template('maori_culture.html', is_logged_in=is_logged_in, user_email=user_email)

@misc_bp.route('/my_bookings')
@login_required
def my_bookings():
    # 获取当前用户的所有事件预订
    event_bookings = EventBooking.query.filter_by(user_id=current_user.id).all()
    
    # 获取当前用户的所有航班预订
    flight_bookings = FlightBooking.query.filter_by(user_id=current_user.id).all()
    
    # 添加登录状态信息
    is_logged_in = current_user.is_authenticated
    user_email = current_user.email if is_logged_in else ''
    
    return render_template('my_bookings.html', 
                           event_bookings=event_bookings, 
                           flight_bookings=flight_bookings,
                           is_logged_in=is_logged_in,
                           user_email=user_email)

@misc_bp.route('/flight_booking_success/<int:booking_id>')
@login_required
def flight_booking_success(booking_id):
    booking = FlightBooking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        abort(403)  # 如果不是当前用户的预订，返回禁止访问
    is_logged_in = current_user.is_authenticated
    user_email = current_user.email if is_logged_in else ''
    return render_template('flight_booking_success.html', booking=booking, is_logged_in=is_logged_in, user_email=user_email)

@misc_bp.route('/booking_success/<int:booking_id>')
@login_required
def booking_success(booking_id):
    booking = EventBooking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        abort(403)  # 如果不是当前用户的预订，返回禁止访问
    is_logged_in = current_user.is_authenticated
    user_email = current_user.email if is_logged_in else ''
    return render_template('booking_success.html', booking=booking, is_logged_in=is_logged_in, user_email=user_email)

@misc_bp.route('/check_login')
def check_login():
    return jsonify({'is_logged_in': current_user.is_authenticated})

@misc_bp.route('/')
def index():
    is_logged_in = current_user.is_authenticated
    user_email = current_user.email if is_logged_in else ''
    return render_template('index.html', is_logged_in=is_logged_in, user_email=user_email)
