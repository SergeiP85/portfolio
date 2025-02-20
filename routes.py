from flask import Blueprint, render_template, redirect, request, url_for, abort
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from models import AboutMeSection, Experience, HeroContent, Page, User, Project, Settings
import json

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def index():
    hero = HeroContent.query.first()
    about_me_section = AboutMeSection.query.first()
    experiences = Experience.query.all()
    projects = Project.query.all()
    settings = Settings.query.first()  # Получаем настройки

    return render_template('index.html', hero=hero, about_me_section=about_me_section, experiences=experiences, projects=projects, show_github=settings.show_github if settings else False)

@app_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin.index'))
    return render_template('login.html')

@app_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app_routes.login'))

@app_routes.route('/page/<int:page_id>')
def show_page(page_id):
    page = Page.query.get_or_404(page_id)
    return render_template('custom_page.html', page=page)

@app_routes.route('/pages/<slug>')
def dynamic_page(slug):
    page = Page.query.filter_by(slug=slug).first()
    if not page:
        abort(404)

    try:
        content_blocks = json.loads(page.content_blocks)
    except json.JSONDecodeError:
        content_blocks = []

    # Проверка структуры JSON
    for block in content_blocks:
        if isinstance(block, dict) and block.get("type") == "image_text_grid":
            print(f"Отладка: block['items'] = {block.get('items')}, тип: {type(block.get('items'))}")

            # Исправление ошибки
            if not isinstance(block.get("items"), list):
                print(f"Ошибка! block['items'] не список, а {type(block.get('items'))}: {block.get('items')}")
                block["items"] = []  # Превращаем в пустой список

    return render_template('page.html', title=page.title, content_blocks=content_blocks)

