from flask import Flask
from flask_migrate import Migrate
from models import db
from routes import app_routes  # Исправляем импорт
from admin import init_admin  # Импортируем инициализацию админки
# from models import AboutMeSection
from flask import request, redirect, url_for, flash


# Инициализация приложения и базы данных
app = Flask(__name__, static_url_path='/static', static_folder='static')


# Конфигурация приложения
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Измените на свой секретный ключ

db.init_app(app)

migrate = Migrate(app, db)

# Подключаем маршруты
app.register_blueprint(app_routes)

# Создание базы данных и таблиц
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    from admin import init_admin
    init_admin(app)
    app.run(debug=True)
