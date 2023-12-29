# app/models.py
from app import db
from app import bcrypt  # Импортируем объект bcrypt

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_type = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    deadline_date = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f"Request('{self.request_type}', '{self.author}', '{self.deadline_date}', '{self.status}', '{self.description}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.email}', '{self.password}')"

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)