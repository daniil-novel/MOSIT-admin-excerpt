# app/__init__.py
from flask import Flask,  render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask import flash


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mirea_kaf_mosit_mosit'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_BINDS'] = {'users': 'sqlite:///users.db'}
app.config['SQLAlCHEMY_TRAC_MODIFICATIONS'] = False
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'authorize'

from app import views  # Импортируем views после инициализации app и db