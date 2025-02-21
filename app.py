from flask import Flask
from flask_migrate import Migrate
from models import db  # Один импорт вместо трех
from routes import app_routes
from admin import init_admin
import os  # Импортируем os для работы с переменными окружения

print("✅ Flask загружен и работает!")

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Получаем URL базы данных из переменной окружения
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')  # Если переменная не установлена, используется SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(app_routes)
init_admin(app)

if __name__ == '__main__':
    app.run(debug=True)
