from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.Text)
    profile_picture = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    purchases = db.relationship('Purchase', backref='user', lazy=True)
    mentorias = db.relationship('Mentorship', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    level = db.Column(db.String(20), nullable=False)  # Iniciante, Intermediário, Avançado
    duration = db.Column(db.Integer, nullable=False)  # Duração em horas
    image = db.Column(db.String(200))
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    modules = db.relationship('Module', backref='course', lazy=True, cascade='all, delete-orphan')
    purchases = db.relationship('Purchase', backref='course', lazy=True)

    def __repr__(self):
        return f'<Course {self.title}>'

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    
    # Relacionamentos
    lessons = db.relationship('Lesson', backref='module', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Module {self.title}>'

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    video_url = db.Column(db.String(200))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    duration = db.Column(db.Integer, nullable=True)  # duração em minutos

    def __repr__(self):
        return f'<Lesson {self.title}>'

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    progress = db.Column(db.Integer, default=0)  # Progresso em porcentagem

    def __repr__(self):
        return f'<Purchase {self.id}>'

class Mentorship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_date = db.Column(db.DateTime)
    notes = db.Column(db.Text) 