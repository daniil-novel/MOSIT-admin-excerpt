# app/__init__.py
from flask import Flask,  render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask import flash
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mirea_kaf_mosit_mosit'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_BINDS'] = {'users': 'sqlite:///users.db', 'user_info': 'sqlite:///user_info.db'}
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'authorize'

# Путь к папке загрузок
app.config['UPLOAD_FOLDER'] = 'uploads'
# Абсолютный путь к папке загрузок
app.config['UPLOAD_FOLDER_PATH'] = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])


from app import views  # Импортируем views после инициализации app и db
