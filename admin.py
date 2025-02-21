### Admin.py
from gc import get_count
from flask import redirect, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user
from markupsafe import Markup
from wtforms import TextAreaField
from models import AboutMeSection, ChatSettings, Experience, HeroContent, Settings, db, User, Page, Project, Reference
import json

# Настройка логина
login_manager = LoginManager()
login_manager.login_view = "app_routes.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Настроим защищенную админку
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('app_routes.login'))
        
        # Получаем данные для статистики
        user_count = User.query.count()
        project_count = Project.query.count()
        experience_count = Experience.query.count()
        
        # Рендерим шаблон с передачей данных
        return self.render('admin/custom_home.html',
                           user_count=user_count,
                           project_count=project_count,
                           experience_count=experience_count, page_count=Page.query.count())


class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('app_routes.login'))

# Настраиваем админку с корректным endpoint
admin = Admin(name='Admin Panel', template_mode='bootstrap3', index_view=MyAdminIndexView())

class ExperienceAdmin(SecureModelView):
    form_columns = ['company_name', 'job_title', 'years', 'description', 'image_url']
    column_list = ['company_name', 'job_title', 'years', 'description', 'image_url']

    # Преобразуем описание в HTML при отображении
    def _format_description(self, context, model, name):
        return Markup(model.description)

    column_formatters = {
        'description': _format_description
    }

class ProjectAdmin(ModelView):
    column_list = ['image_url', 'link_url', 'description']
    form_columns = ['image_url', 'link_url', 'description']
    column_searchable_list = ['description']
    column_filters = ['link_url']

class PageAdmin(SecureModelView):
    column_list = ['title', 'slug', 'content_blocks']
    form_overrides = {
        'content_blocks': TextAreaField
    }
    form_args = {
        'content_blocks': dict(description='Введите блоки в формате JSON (например: [{"type": "text", "content": "Привет"}])')
    }

    def on_model_change(self, form, model, is_created):
        # Валидация и форматирование JSON
        import json
        try:
            parsed = json.loads(model.content_blocks)
            if not isinstance(parsed, list):
                raise ValueError("content_blocks должен быть списком JSON-объектов.")
            model.content_blocks = json.dumps(parsed, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            raise ValueError("Ошибка при парсинге JSON: Проверьте правильность структуры.")

class SettingsAdmin(ModelView):
    form_excluded_columns = ('id',)
    column_labels = {'show_github': 'Show GitHub Section'}

class ReferenceAdmin(ModelView):
    column_list = ['quote', 'reviewer', 'position', 'linkedin_url', 'image_url']
    form_columns = ['quote', 'reviewer', 'position', 'linkedin_url', 'image_url']

class ChatSettingsAdmin(ModelView):
    form_overrides = {
        'description': TextAreaField,
    }
    form_columns = ('description', 'is_visible')
    can_create = True
    can_delete = True
    column_labels = {'is_visible': 'Show Chatbot'}

# Регистрируем админку
def register_admin(admin):
    admin.add_view(PageAdmin(Page, db.session))

# Инициализация админки
def init_admin(app):
    login_manager.init_app(app)
    admin.init_app(app)
    admin.add_view(SecureModelView(Page, db.session))
    admin.add_view(SecureModelView(HeroContent, db.session))
    admin.add_view(SecureModelView(AboutMeSection, db.session))
    admin.add_view(SecureModelView(Experience, db.session))
    admin.add_view(ProjectAdmin(Project, db.session))
    admin.add_view(SecureModelView(User, db.session, name='Users'))
    admin.add_view(SettingsAdmin(Settings, db.session, name="GitHub Settings"))
    admin.add_view(ReferenceAdmin(Reference, db.session))
    admin.add_view(ChatSettingsAdmin(ChatSettings, db.session))