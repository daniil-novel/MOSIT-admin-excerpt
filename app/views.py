# app/views.py
from flask import flash, render_template, request, redirect, url_for
from app import app, db, login_manager
from app.models import Request, User
from flask_login import login_user, logout_user, login_required, current_user
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    requests = Request.query.all()
    return render_template('index.html', requests=requests)

@app.route('/profile')
def profile():
    return render_template("profile.html")


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        # Получаем данные из формы
        type_value = request.form['type']
        author_value = request.form['author']
        deadline_value = request.form['deadline']
        status_value = request.form['status']
        description_value = request.form['description']

        # Обработка файла
        if 'attachment' not in request.files:
            flash('Файл не выбран', 'danger')
            return redirect(request.url)

        file = request.files['attachment']

        if file.filename == '':
            flash('Файл не выбран', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Недопустимый формат файла', 'danger')
            return redirect(request.url)

        # Cохранение в базу данных
        new_request = Request(
            request_type=type_value,
            author=author_value,
            deadline_date=deadline_value,
            status=status_value,
            description=description_value,
            attachment=filename
        )
        db.session.add(new_request)
        db.session.commit()

        # После сохранения, перенаправляем на страницу индекса
        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        # Используем метод get() для избежания ошибки, если 'request_id' отсутствует в запросе
        request_id = request.form.get('request_id')
        deadline_value = request.form.get('deadline')
        status_value = request.form.get('status')
        description_value = request.form.get('description')

        if request_id is None:
            flash('Не удалось получить идентификатор заявки', 'danger')
            return redirect(url_for('index'))

        # Обработка файла
        if 'attachment' in request.files:
            file = request.files['attachment']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                flash('Недопустимый формат файла', 'danger')
                return redirect(request.url)
        else:
            filename = None  # Оставляем текущий файл без изменений

        # Обновление данных в базе данных
        request_data = Request.query.get(request_id)

        # Проверяем, найдена ли запись
        if request_data is None:
            flash('Заявка с указанным идентификатором не найдена', 'danger')
            return redirect(url_for('index'))

        request_data.deadline_date = deadline_value
        request_data.status = status_value
        request_data.description = description_value

        if filename:
            request_data.attachment = filename  # Обновление имени файла, если загружен новый файл

        db.session.commit()

        # Перенаправление на страницу индекса
        return redirect(url_for('index'))

    # Если GET-запрос, просто отображаем форму редактирования
    return render_template('edit.html', **request.form)


@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first() # Представляем email в качестве юзера, который заходит на сайт

        if user and user.check_password(password):
            login_user(user)
            flash('Успешная авторизация!', 'success')
            return redirect(url_for('main_index'))
        else:
            flash('Неверные учетные данные. Попробуйте еще раз.', 'danger')

    return render_template('authorize.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы.', 'info')
    return redirect(url_for('authorize'))

@app.route('/')
@login_required
def main_index():
    if current_user.is_authenticated and current_user.email == 'zhenya@gmail.com':
        # Если пользователь аутентифицирован и его email равен 'zhenya@gmail.com',
        # отображаем все заявки
        requests_data = Request.query.all()
    else:
        # Иначе, отображаем только заявки текущего пользователя
        requests_data = Request.query.filter_by(author=current_user.email).all()

    return render_template('index.html', requests=requests_data)