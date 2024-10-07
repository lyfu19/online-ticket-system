from flask import Blueprint, render_template, request, redirect, url_for, flash
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