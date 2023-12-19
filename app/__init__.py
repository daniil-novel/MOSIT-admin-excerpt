# app/__init__.py
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Используйте свой URI для базы данных
db = SQLAlchemy(app)

# Модель для базы данных
class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_type = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    deadline_date = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)  # Добавлено поле для описания

# Добавим вывод в консоль при создании базы данных
with app.app_context():
    db.create_all()
    print("База данных успешно создана!")

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


@app.route('/')
def main_index():
    # Получаем данные для отображения на странице
    requests_data = [
        {"request_type": "Тип 1", "author": "Автор 1", "deadline_date": "01-01-2023", "status": "Отправлена", "description": "Описание 1"},
        {"request_type": "Тип 2", "author": "Автор 2", "deadline_date": "02-01-2023", "status": "Принята", "description": "Описание 2"},
        {"request_type": "Тип 3", "author": "Автор 3", "deadline_date": "03-01-2023", "status": "Выполнена", "description": "Описание 3"},
    ]

    return render_template('index.html', requests=requests_data)