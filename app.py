from flask import Flask
import logging
from config import Config, configure_login, configure_babel
from views.auth import auth_bp
from views.event import event_bp
from views.flight import flight_bp
from views.misc import misc_bp
from fake_data import populate_database

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth_bp)
app.register_blueprint(event_bp)
app.register_blueprint(flight_bp)
app.register_blueprint(misc_bp)

# 设置日志
logging.basicConfig(level=logging.DEBUG)

configure_login(app)
configure_babel(app)
populate_database(app)

if __name__ == '__main__':
    app.run(debug=True)