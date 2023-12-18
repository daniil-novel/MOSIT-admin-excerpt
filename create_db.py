# create_db.py
from app import create_app, db

# Создаем Flask-приложение
app = create_app()

# Обновим контекст приложения
with app.app_context():
    # Создаем все таблицы в базе данных
    db.create_all()

