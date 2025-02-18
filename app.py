### app.py
from flask import Flask
from flask_migrate import Migrate
from models import db
from routes import app_routes
from admin import init_admin

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(app_routes)

with app.app_context():
    db.create_all()

init_admin(app)

if __name__ == '__main__':
    app.run(debug=True)
