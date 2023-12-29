# app/__init__.py
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt  # Добавим импорт для Flask-Bcrypt
from flask import flash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mirea_kaf_mosit_mosit'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # База данных для заявок
app.config['SQLALCHEMY_BINDS'] = {'users': 'sqlite:///users.db'}  # База данных для пользователей
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)  # Инициализация Flask-Bcrypt

login_manager = LoginManager(app)
login_manager.login_view = 'authorize'


# Модель для базы данных заявок
class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_type = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    deadline_date = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)


# Модель для базы данных пользователей
class User(db.Model, UserMixin):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"User('{self.email}', '{self.password}')"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ваш код Flask, где происходит обращение к базе данных
@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Проверяем, есть ли пользователь с таким email в базе данных
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # Пользователь найден - производим авторизацию
            login_user(user)
            flash('Успешная авторизация!', 'success')
            return redirect(url_for('main_index'))
        else:
            # Пользователь не найден - выводим сообщение об ошибке
            flash('Неверные учетные данные. Попробуйте еще раз.', 'danger')

    return render_template('authorize.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Получаем данные из формы
        type_value = request.form['type']
        author_value = request.form['author']
        deadline_value = request.form['deadline']
        status_value = request.form['status']
        description_value = request.form['description']

        # Здесь вы можете добавить код для сохранения в базу данных, если необходимо
        new_request = Request(
            request_type=type_value,
            author=author_value,
            deadline_date=deadline_value,
            status=status_value,
            description=description_value
        )
        db.session.add(new_request)
        db.session.commit()

        # После сохранения, перенаправляем на страницу индекса
        return redirect(url_for('main_index'))

    return render_template('create.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        # Обработка данных из формы редактирования
        # В данном случае, мы пока не сохраняем данные, а просто отображаем их в форме
        return render_template('edit.html', **request.form)

    # Если GET-запрос, просто отображаем форму редактирования
    return render_template('edit.html')


# Обновляем main_index для перенаправления на index.html после успешной авторизации
@app.route('/')
@login_required
def main_index():
    return render_template('index.html', requests=requests_data)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы.', 'info')
    return redirect(url_for('authorize'))