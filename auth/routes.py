from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from models import User, db, Concert, ConcertTicket, TicketType
from . import auth_blueprint  # 这里导入已经定义好的蓝图
from flask_login import login_user, logout_user, current_user, login_required
from flask import jsonify  # 引入 jsonify 函数
from datetime import datetime, timezone

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()  # 获取 JSON 数据
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # 检查输入是否为空
        if not username or not email or not password:
            return jsonify({"message": "Please fill out all fields!"}), 400

        # 检查是否存在相同的用户名或电子邮件
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            return jsonify({"message": "Username or email already exists!"}), 400

        # 创建新用户并保存到数据库
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Registration successful!"}), 200  # 返回 JSON 数据

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()  # 获取JSON数据
        username = data.get('username')
        password = data.get('password')

        # 查询用户
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # 使用 Flask-Login 登录用户
            login_user(user)  # 这一行取代手动的 session['user_id']
            print(f"User {user.username} logged in")  # 添加调试信息
            return jsonify({"message": "Login successful!"}), 200
        else:
            flash('Login failed, please try again.')
            return jsonify(message="Invalid username or password!"), 401

@auth_blueprint.route('/logout')
def logout():
    logout_user()  # Flask-Login 提供的登出方法，清除会话
    flash('You have been logged out.')
    next_page = request.args.get('next', url_for('home'))
    return redirect(next_page)

@auth_blueprint.route('/settings', methods=['GET', 'POST'])
@login_required  # 确保用户必须登录才能访问设置
def settings():
    user = current_user

    if request.method == 'POST':
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        email = data.get('email')

        # 验证当前密码
        if not check_password_hash(user.password, current_password):
            return jsonify({"message": "Current password is incorrect!"}), 400

        # 更新邮箱
        if email:
            user.email = email

        # 如果用户输入了新密码，更新密码
        if new_password:
            hashed_password = generate_password_hash(new_password)
            user.password = hashed_password

        db.session.commit()

        # 重新登录用户以确保 current_user 的信息是最新的
        login_user(user)  # 重新登录用户，刷新 current_user 数据

        return jsonify({"message": "Settings updated successfully!"}), 200

    return jsonify({"message": "Settings page"}), 200

@auth_blueprint.route('/concerts/<int:concert_id>')
def concert_detail(concert_id):
    concert = Concert.query.get_or_404(concert_id)
    return render_template('concert_detail.html', concert=concert)

@auth_blueprint.route('/purchase_ticket', methods=['POST'])
def purchase_ticket():
    if not current_user.is_authenticated:
        return jsonify({'message': 'Please log in to purchase tickets.'}), 401
    
    data = request.get_json()
    ticket_type_str = data.get('ticket_type')
    concert_id = int(data.get('concert_id'))
    ticket_quantity = int(data.get('ticket_quantity', 1))  # 默认购票数量为1

    if not ticket_type_str or not concert_id:
        return jsonify({"message": "Please select a ticket type and concert!"}), 400

    # 将票务类型字符串转换为枚举类型
    try:
        ticket_type = TicketType(ticket_type_str)  # 确保 ticket_type 是枚举类型
    except ValueError:
        return jsonify({"message": "Invalid ticket type!"}), 400
    
    # 获取演唱会
    concert = Concert.query.get(concert_id)
    if not concert:
        return jsonify({"message": "Concert not found!"}), 404

    # 检查余票
    if concert.available_tickets < ticket_quantity:
        return jsonify({"message": "Not enough tickets available!"}), 400

    # 创建 ConcertTicket 对象
    for _ in range(ticket_quantity):
        new_ticket = ConcertTicket(
            concert_id=concert_id,
            user_id=current_user.id,
            seat_number=generate_seat_number(concert_id),  # 生成座位号
            ticket_type=ticket_type,  # 使用枚举类型
            ticket_price=get_ticket_price(concert, ticket_type),
            purchase_date=datetime.now(timezone.utc)
        )
        db.session.add(new_ticket)
    concert.available_tickets -= int(ticket_quantity)
    db.session.commit()

    return jsonify({"message": "Purchase successful!"}), 200

# 这个函数用来生成座位号（你可以根据你的逻辑定义）
def generate_seat_number(concert_id):
    # 这里使用一个简单的座位号生成逻辑
    return f"SN-{concert_id}-{int(datetime.now().timestamp()) % 1000}"

# 这个函数根据票务类型获取票价
def get_ticket_price(concert, ticket_type):
    if ticket_type == TicketType.VIP:
        return concert.vip_ticket_price
    else:
        return concert.regular_ticket_price

# 这个函数模拟检查是否有余票（根据你需要的逻辑处理）
def get_available_tickets(concert_id, ticket_type):
    # 假设你有一种方式检查特定票种的余票数量
    return 100000  # 这里是假设有10张余票