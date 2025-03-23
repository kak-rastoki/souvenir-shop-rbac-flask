"""
Модуль авторизации и регистрации
--------------------------------------------------
Описание:

"""


from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template,url_for,request,session,redirect,flash
from . import auth_bp
from app import db, Users


@auth_bp.route('/signup', methods=['GET']) # Вывод страницы авторизации \ регистрации
def signup():
    return render_template('reg.html', errors={})



# Кнопка зарегистрироваться
@auth_bp.route('/registration', methods=['POST'])
def registration():
    nick_name = request.form.get('full_nameSign')
    phone = request.form.get('phone')
    password = request.form.get('passwordSign')
    confirm_password = request.form.get('confirm_passwordSign')
    email = request.form.get('emailSign')

    #проверки
    error_messages = {}
    if not nick_name or not phone or not password or not confirm_password or not email:
        error_messages["general"] = "В форме есть ошибки заполнения. \n Пожалуйста проверьте поля.Все поля необходимо заполнить по условиям"
    if len(password) < 8:
        error_messages["password_len"] = "Пароль должен содержать более 8 символов"
    if Users.query.filter_by(mail_user=email).first():
        error_messages["email"] = "Пользователь с таким email уже существует."
    if Users.query.filter_by(phone_number=phone).first():
        error_messages["phone"] = "Пользователь с таким номером телефона уже существует"
    if Users.query.filter_by(Name_user= nick_name).first():
        error_messages["nick_name"] = "Пользователь с таким именем уже существует"
    if password != confirm_password:
        error_messages["password_confirmed"] = "Введенные пароли не совпадают"

    if error_messages:
        return render_template("reg.html", errors=error_messages, form=request.form)


    # создание пользователя
    new_user = Users(
        Name_user=nick_name,
        phone_number=phone,
        hash_user=generate_password_hash(password),
        mail_user=email,
        role='user'

    )

    # добавление дефолтного аватара
    with open('static/img/default_avatar.png', 'rb') as f:
       new_user.avatar = f.read()

    db.session.add(new_user)
    db.session.commit()

    flash("Регистрация прошла успешно! Теперь вы можете войти.", "success")
    return redirect('auth.signup')

@auth_bp.route('/login', methods = ['POST'])
def login():

    email = request.form.get('email')
    password = request.form.get('password1')
    user = Users.query.filter_by(mail_user=email).first()
    print(f"ДАННЫЕ С ФОРМЫ ПОЛУЧЕНЫ")


    if not user or  check_password_hash(user.hash_user, password) != True:
        flash("Неверный логин или пароль", "errorLogin")
        print("проверка не прошла")
        return redirect(url_for('auth.signup'))

    session.clear()
    login_user(user)
    print(f'Пользователь: {user.Name_user} - авторизован')
    return redirect(url_for('index'))

@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('index'))
