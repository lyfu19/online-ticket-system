from flask import session, request, redirect, url_for
from flask_babel import Babel

# 初始化 Flask-Babel 对象
babel = Babel()

# 设置支持的语言
LANGUAGES = {
    'en': 'English',
    'mi': 'Māori'
}

# Babel 语言选择器函数，从 session 中获取语言
def get_locale():
    return session.get('lang', request.accept_languages.best_match(LANGUAGES.keys()))

# 初始化 Babel，并将语言选择器函数传入
def init_babel(app):
    babel.init_app(app, locale_selector=get_locale)

# 设置语言的路由函数
def set_language_route(app):
    @app.route('/set_language/<lang>')
    def set_language(lang):
        if lang not in LANGUAGES:
            lang = 'en'  # 如果选择了不支持的语言，默认使用英语
        session['lang'] = lang
        return redirect(request.referrer or url_for('home'))