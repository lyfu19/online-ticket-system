# views/auth.py
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from database import db
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({'success': False, 'message': 'Email already exists.'}), 400
        
        # 修改这一行
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        current_app.logger.info(f"User registered successfully: {email}")
        return jsonify({'success': True, 'message': 'Registration successful. Please log in.'}), 200
    except Exception as e:
        current_app.logger.error(f"Error during registration: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': 'An error occurred during registration.'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    try:
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            current_app.logger.info(f"User logged in successfully: {email}")
            return jsonify({'success': True, 'message': 'Login successful.', 'email': email}), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password.'}), 401
    except Exception as e:
        current_app.logger.error(f"Error during login: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred during login.'}), 500

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'success': True})