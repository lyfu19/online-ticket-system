from flask import Flask
from flask_migrate import Migrate
from config import Config
from models import db
from auth import auth_blueprint
from views import inject_user, home, concerts

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

# 注册 inject_user 和路由
app.context_processor(inject_user)
app.route('/')(home)
app.route('/concerts')(concerts)

app.register_blueprint(auth_blueprint, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)