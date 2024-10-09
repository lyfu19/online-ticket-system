from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from models import db, User
from auth import auth_blueprint
from views import home, concerts

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

# 初始化 Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# 用户加载函数，Flask-Login 自动调用
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 注册 inject_user 和路由
app.route('/')(home)
app.route('/concerts')(concerts)

app.register_blueprint(auth_blueprint, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)