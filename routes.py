from flask import current_app
from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from models import Page, db, AboutMeSection, Experience, HeroContent, User, Project, Settings, ChatSettings, Reference

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def index():
    hero = HeroContent.query.first()
    about_me_section = AboutMeSection.query.first()
    experiences = Experience.query.all()
    projects = Project.query.all()
    settings = Settings.query.first()  # Получаем настройки
    references = Reference.query.all()
    chat_settings = ChatSettings.query.first()
    
    print(chat_settings)  # Печать данных для отладки

    return render_template('index.html', hero=hero, about_me_section=about_me_section, experiences=experiences, projects=projects, chat_settings=chat_settings, show_github=settings.show_github if settings else False, references=references)

# Используем app_routes для маршрута /page/<slug>
@app_routes.route('/page/<slug>')
def show_page(slug):
    try:
        page = Page.query.filter_by(slug=slug).first_or_404()
        content_blocks = page.get_content_blocks()  # Получаем блоки из модели
        return render_template('page_template.html', page=page, content_blocks=content_blocks)
    except Exception as e:
        current_app.logger.error(f"Ошибка при загрузке страницы с slug {slug}: {e}")
        return render_template('errors/500.html'), 500


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

@app_routes.route('/add_reference', methods=['POST'])
def add_reference():
    quote = request.form.get('quote')
    reviewer = request.form.get('reviewer')
    position = request.form.get('position')
    linkedin_url = request.form.get('linkedin_url')
    image_url = request.form.get('image_url')

    new_reference = Reference(
        quote=quote, reviewer=reviewer, position=position,
        linkedin_url=linkedin_url, image_url=image_url
    )
    db.session.add(new_reference)
    db.session.commit()
    
    return redirect(url_for('app_routes.references'))
