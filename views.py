from flask import render_template, session
from models import User

# 注入 current_user
def inject_user():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        print(f"Injecting user: {user}")  # 调试输出
        return dict(current_user=user)
    print("No user to inject")  # 如果没有用户
    return dict(current_user=None)

# 首页路由
def home():
    print(f"Session contains: {session}")
    return render_template('index.html')