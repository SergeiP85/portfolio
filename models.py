### models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    content_blocks = db.Column(db.Text, nullable=False, default='[]')  # Храним JSON в текстовом формате



class HeroContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    hidden_text = db.Column(db.Text, nullable=True)
    resume_link = db.Column(db.String(255), nullable=False)
    email_link = db.Column(db.String(255), nullable=False)
    github_link = db.Column(db.String(255), nullable=False)
    linkedin_link = db.Column(db.String(255), nullable=False)

class AboutMeSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), default="A bit about me")
    content = db.Column(db.Text, nullable=False)

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    years = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(300), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)  # Ссылка на картинку
    link_url = db.Column(db.String(255), nullable=False)   # Ссылка для перехода
    description = db.Column(db.Text, nullable=False)       # Описание проекта

    def __repr__(self):
        return f"<Project {self.description[:30]}...>"

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_github = db.Column(db.Boolean, default=True)  # Флаг видимости

    def __repr__(self):
        return f"<Settings show_github={self.show_github}>"

class Reference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.Text, nullable=False)
    reviewer = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=False)
    linkedin_url = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(355), nullable=True)
