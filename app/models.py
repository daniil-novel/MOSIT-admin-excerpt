# app/models.py
from flask_login import UserMixin
from app import db
from app import bcrypt  # Импортируем объект bcrypt


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_type = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    deadline_date = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    attachment = db.Column(db.String(255), nullable=True)


    def __repr__(self):
        return f"Request('{self.request_type}', '{self.author}', '{self.deadline_date}', '{self.status}', '{self.description}')"

class User(db.Model, UserMixin):
    __bind_key__ = 'users'
    __tablename__ = 'user'  # явное указание имени таблицы
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fio = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.email}', '{self.fio}', '{self.password}')"

    def __init__(self, email, fio, password):
        self.email = email
        self.fio = fio
        self.password = self.generate_password_hash(password)

    def generate_password_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=12).decode('utf-8')
    
    def check_password(self, password_to_check):
        #return bcrypt.check_password_hash(self.password, password_to_check)
        return bcrypt.check_password_hash(self.generate_password_hash(self.password), password_to_check)
    
    def update_password(self, new_password):
        self.password = self.generate_password_hash(new_password)
