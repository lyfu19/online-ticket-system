# views/event.py
from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import current_user, login_required
from database import db
from models import Event, EventBooking
from flask_paginate import Pagination, get_page_parameter

event_bp = Blueprint('event', __name__)

@event_bp.route('/events')
def events():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    offset = (page - 1) * per_page
    total_events = Event.query.count()
    events = Event.query.order_by(Event.date).offset(offset).limit(per_page).all()
    
    total_pages = -(-total_events // per_page)  # 向上取整
    
    pagination = Pagination(page=page, total=total_events, per_page=per_page, css_framework='')
    
    is_logged_in = current_user.is_authenticated
    user_email = current_user.email if is_logged_in else ''
    
    return render_template('events.html', events=events, pagination=pagination, 
                           total_pages=total_pages, is_logged_in=is_logged_in, 
                           user_email=user_email)

@event_bp.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    is_logged_in = current_user.is_authenticated
    user_email = current_user.email if is_logged_in else ''
    return render_template('event_detail.html', event=event, is_logged_in=is_logged_in, user_email=user_email)

@event_bp.route('/book_ticket', methods=['POST'])
@login_required
def book_ticket():
    data = request.get_json()
    event_id = data.get('event_id')
    quantity = data.get('quantity')

    event = Event.query.get_or_404(event_id)
    
    new_booking = EventBooking(user_id=current_user.id, event_id=event_id, quantity=quantity)
    db.session.add(new_booking)
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': 'Event booked successfully!', 'booking_id': new_booking.id}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error booking event: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred while booking the event.'}), 500