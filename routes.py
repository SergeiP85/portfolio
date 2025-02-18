### routes.py
from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from models import AboutMeSection, Experience, HeroContent, Page, User, Project

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def index():
    hero = HeroContent.query.first()
    about_me_section = AboutMeSection.query.first()
    experiences = Experience.query.all()
    projects = Project.query.all()

    # Отладка
    print(f"Hero: {hero}")
    print(f"Projects found: {len(projects)}")
    for p in projects:
        print(f"{p.id}: {p.image_url} | {p.link_url} | {p.description}")

    return render_template('index.html', hero=hero, about_me_section=about_me_section, experiences=experiences, projects=projects)


@app_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin.index'))  # Исправлено на admin.index без кастомного endpoint
    return render_template('login.html')

@app_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app_routes.login'))

@app_routes.route('/page/<int:page_id>')
def view_page(page_id):
    page = Page.query.get_or_404(page_id)
    return render_template('page.html', page=page)