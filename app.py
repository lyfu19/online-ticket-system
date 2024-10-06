from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{Config.DB_USER}:{Config.DB_PASSWORD}@localhost/{Config.DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # 初始化 Flask-Migrate

@app.route('/')
def home():
    return render_template('index.html')

from sqlalchemy import text

@app.route('/test')
def test_connection():
    try:
        # 测试连接，执行简单的 SQL 语句
        result = db.session.execute(text('SELECT 1'))  # 使用 text() 包装 SQL 语句
        return "Successfully connected to the database!" if result.fetchone() else "Connection failed."
    except Exception as e:
        return f"Connection failed: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)