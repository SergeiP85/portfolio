from flask import Flask
from flask_migrate import Migrate
from models import db
from routes import app_routes
from admin import init_admin

print("✅ Flask загружен и работает!")

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Указываем URL базы данных напрямую, например, SQLite:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Секретный ключ напрямую

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(app_routes)
init_admin(app)

# Запуск приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
