from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from models import User, db
from . import auth_blueprint  # 这里导入已经定义好的蓝图

from flask import jsonify  # 引入 jsonify 函数

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

    return render_template('register.html')  # 对于 GET 请求，返回模板

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()  # 获取JSON数据
        username = data.get('username')
        password = data.get('password')

        # 查询用户
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # 登录成功，将用户ID存储到session中
            session['user_id'] = user.id
            print(f"User {user.username} logged in with session ID: {session['user_id']}")  # 添加调试信息
            return jsonify(message="Login successful!"), 200
        else:
            flash('Login failed, please try again.')
            return jsonify(message="Invalid username or password!"), 401

    return render_template('login.html')

@auth_blueprint.route('/logout')
def logout():
    session.pop('user_id', None)  # 清除用户会话
    flash('You have been logged out.')
    return redirect(url_for('home'))