# app/views.py
from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Request, User
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
def index():
    requests = Request.query.all()
    return render_template('index.html', requests=requests)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        request_type = request.form['request_type']
        author = request.form['author']
        deadline_date = request.form['deadline_date']
        status = request.form['status']
        description = request.form['description']  

        new_request = Request(
            request_type=request_type,
            author=author,
            deadline_date=deadline_date,
            status=status,
            description=description 
        )
        db.session.add(new_request)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    req_to_edit = Request.query.get(id)

    if request.method == 'POST':
        req_to_edit.request_type = request.form['type']
        req_to_edit.author = request.form['author']
        req_to_edit.deadline_date = request.form['deadline']
        req_to_edit.status = request.form['status']
        req_to_edit.description = request.form['description']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', request=req_to_edit)

@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']  # Добавим поле для ввода пароля

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Успешная авторизация!', 'success')
            return redirect(url_for('main_index'))
        else:
            flash('Неверные учетные данные. Попробуйте еще раз.', 'danger')

    return render_template('authorize.html')