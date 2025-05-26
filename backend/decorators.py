from functools import wraps
from flask import abort, current_app, jsonify, flash, redirect, url_for
from flask_login import current_user

# зашита админских роутов
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.role == 'admin':
            abort(403)
        return fn(*args, **kwargs)
    return wrapper

#неавторизованно ошибка для API
def custom_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Пожалуйста, войдите в систему', 'status': 401}), 401
        return f(*args, **kwargs)
    return decorated_function

# зашита роутов продавца
def seller_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        if not current_user.is_authenticated or current_user.role not in ['seller', 'admin']:
            flash('У вас нет прав доступа к панели продавца.', 'danger') # Добавлено сообщение

            abort(403)
        return fn(*args, **kwargs)
    return wrapper
