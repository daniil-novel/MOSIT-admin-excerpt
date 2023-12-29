# app/views.py
from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Request, User


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
        username = request.form['username']

        # Проверяем, существует ли пользователь в базе данных
        user = User.query.filter_by(email=email, username=username).first()

        if user:
            # Пользователь существует, перенаправляем на главную страницу
            return redirect(url_for('main_index'))

    return render_template('authorize.html')