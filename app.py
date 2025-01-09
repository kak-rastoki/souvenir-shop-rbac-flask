from flask import Flask, render_template,url_for, send_file,redirect, request, jsonify, session,flash,get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
import io
from datetime import datetime
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///woodyDB.db'
app.secret_key = '1111'
db = SQLAlchemy(app)

# DB Models


class Genders(db.Model):
    __tablename__ = 'Genders'
    ID_gender = db.Column(db.Integer, primary_key=True)
    gender_name = db.Column(db.String, nullable=False)
    short_name = db.Column(db.String)

class Users(db.Model):
    __tablename__ = 'Users'
    ID_user = db.Column(db.Integer, primary_key=True)
    Name_user = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String)
    hash_user = db.Column(db.String, nullable=False)
    mail_user = db.Column(db.String, nullable=False, unique=True)
    BirthDay_user = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    id_gender = db.Column(db.Integer, db.ForeignKey('Genders.ID_gender'))

    gender = db.relationship('Genders', backref='users')

class Categories(db.Model):
    __tablename__ = 'Categories'
    ID_categories = db.Column(db.Integer, primary_key=True)
    Name_category = db.Column(db.String, nullable=False)
    Discription_category = db.Column(db.Text)

class Masters(db.Model):
    __tablename__ = 'Masters'
    ID_master = db.Column(db.Integer, primary_key=True)
    Name_master = db.Column(db.String, nullable=False)
    id_gender = db.Column(db.Integer, db.ForeignKey('Genders.ID_gender'))

    gender = db.relationship('Genders', backref='masters')

class Product(db.Model):
    __tablename__ = 'Product'

    ID_product = db.Column(db.Integer, primary_key=True)
    Name_product = db.Column(db.String, nullable=False)
    Cost_product = db.Column(db.Integer, nullable=False)
    Description_product = db.Column(db.Text, nullable=True)
    id_category = db.Column(db.Integer, db.ForeignKey('Categories.ID_categories'), nullable=False)
    id_master = db.Column(db.Integer, db.ForeignKey('Masters.ID_master'), nullable=False)
    IsNew_product = db.Column(db.Boolean, default=True)
    image_product = db.Column(db.LargeBinary, nullable=True)

    category = db.relationship('Categories', backref=db.backref('products', lazy=True))
    master = db.relationship('Masters', backref=db.backref('products', lazy=True))

class Favorite(db.Model):
    __tablename__ = 'Favorite'
    ID_favorite = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('Users.ID_user'))
    id_product = db.Column(db.Integer, db.ForeignKey('Product.ID_product'))

    user = db.relationship('Users', backref='favorites')
    product = db.relationship('Product', backref='favorited_by')

class Review(db.Model):
    __tablename__ = 'Review'
    ID_favorite = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('Users.ID_user'))
    id_product = db.Column(db.Integer, db.ForeignKey('Product.ID_product'))

    user = db.relationship('Users', backref='reviews')
    product = db.relationship('Product', backref='reviews')

class Currency(db.Model):
    __tablename__ = 'Currency'
    ID_currency = db.Column(db.Integer, primary_key=True)
    currency_name = db.Column(db.String, nullable=False)
    symbol = db.Column(db.String, nullable=False)

class Order(db.Model):
    __tablename__ = 'Order'
    ID_order = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('Users.ID_user'))
    Data_order = db.Column(db.Date)
    Status_order = db.Column(db.Boolean, default=False)

    user = db.relationship('Users', backref='orders')

class OrderProduct(db.Model):
    __tablename__ = 'OrderProduct'
    ID_OP = db.Column(db.Integer, primary_key=True)
    id_order = db.Column(db.Integer, db.ForeignKey('Order.ID_order'))
    id_product = db.Column(db.Integer, db.ForeignKey('Product.ID_product'))
    id_currency = db.Column(db.Integer, db.ForeignKey('Currency.ID_currency'))
    quantity = db.Column(db.Integer, nullable=False)

    order = db.relationship('Order', backref='order_products')
    product = db.relationship('Product', backref='ordered_in')
    currency = db.relationship('Currency', backref='order_products')


#маршруты
@app.route('/product_image/<int:product_id>')
def product_image(product_id):
    product = Product.query.get_or_404(product_id)
    return send_file(io.BytesIO(product.image_product), mimetype='image/jpeg')


@app.route('/product/<int:product_id>')
def productCard(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@app.route('/')
def index():
    productNew = Product.query.filter_by(IsNew_product=1).all()
    return render_template('main.html', productNew=productNew)

@app.route('/base')
def showBase():
    return render_template('base.html')

# ------------- АДМИН-ПАНЕЛЬ -------------------- #
@app.route('/admin')
def Admin_products():
    masters = Masters.query.all()
    categories = Categories.query.all()
    products = Product.query.all()
    # errors2 = request.args.get('errors2',{})

    products_data = []
    for product in products:

        category = Categories.query.get(product.id_category)
        master = Masters.query.get(product.id_master)


        products_data.append({
            'ID_product': product.ID_product,
            'Name_product': product.Name_product,
            'Cost_product': product.Cost_product,
            'Description_product': product.Description_product,
            'Category_name': category.Name_category if category else 'Неизвестно', # Заменяем ID на имя
            'Master_name': master.Name_master if master else 'Неизвестно',
            'IsNew_product': product.IsNew_product
        })

        print (products_data)

    errors1 = get_flashed_messages(category_filter=['error1'])
    if not errors1:
        errors1 = {}
    errors2=get_flashed_messages(category_filter=['error2'])
    if not errors2:
        errors2 = {}


    return render_template('admin/A_products.html', masters=masters, categories=categories, products=products_data, errors2=errors2,errors1=errors1)

@app.route('/admin/add-product', methods=['GET', 'POST'])
def AP_add_product():

    errors2=get_flashed_messages(category_filter=['error'])
    if not errors2:
        errors2 = {}

    masters = Masters.query.all()
    categories = Categories.query.all()
    #  Получаем все товары
    products = Product.query.all()
    products_data = []
    for product in products:
        #  связанные категорию и мастера для каждого товара
        category = Categories.query.get(product.id_category)
        master = Masters.query.get(product.id_master)


        products_data.append({
            'ID_product': product.ID_product,
            'Name_product': product.Name_product,
            'Cost_product': product.Cost_product,
            'Description_product': product.Description_product,
            'Category_name': category.Name_category if category else 'Неизвестно',  # Заменяем ID на имя
            'Master_name': master.Name_master if master else 'Неизвестно',
            'IsNew_product': product.IsNew_product
        })

    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        new_product = request.form.get('newProduct') == 'on'
        master = request.form.get('master')
        category = request.form.get('category')

        if not name or not price:
            flash("Все поля, кроме 'Новинка', обязательны для заполнения!", "error")
            return redirect(url_for('AP_add_product'))

        if category == "Выберите категорию" or master == "Выберите мастера":
            flash("Пожалуйста, выберите категорию и мастера!", "error")
            return redirect(url_for('AP_add_product'))

        try:
            price = float(price)  # Проверяем, что цена - число
        except ValueError:
            flash("Цена должна быть числом!", "error")
            return redirect(url_for('AP_add_product'))

        # Сохранение в базу данных
        new_product_entry = Product(
            Name_product=name,
            Cost_product=price,
            IsNew_product=new_product,
            id_master=master,
            id_category=category,
        )
        db.session.add(new_product_entry)
        db.session.commit()

        flash("Товар успешно добавлен!", "success")
        return redirect(url_for('Admin_products'))

    return render_template('admin/A_products.html', masters=masters, categories=categories,products=products_data,errors2=errors2)

@app.route('/admin/products_table',methods=['GET'])
def display_products():
     # Получаем все товары
    products = Product.query.all()

    # Подготавливаем данные о товарах для передачи в шаблон
    products_data = []
    for product in products:
        # Получаем связанные категорию и мастера для каждого товара
        category = Categories.query.get(product.id_category)
        master = Masters.query.get(product.id_master)

        # Создаем словарь с данными
        products_data.append({
            'ID_product': product.ID_product,
            'Name_product': product.Name_product,
            'Cost_product': product.Cost_product,
            'Description_product': product.Description_product,
            'Category_name': category.Name_category if category else 'Неизвестно', # Заменяем ID на имя
            'Master_name': master.Name_master if master else 'Неизвестно', # Заменяем ID на имя
            'IsNew_product': product.IsNew_product
        })

    return render_template('admin/A_products.html',products=products_data)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_product(id):
    product= Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        print (f'Продукт {product.ID_product} - {product.Name_product} успешно удален')
    else:
        print (f'Внутренняя ошибка сервера. Продукт {product.ID_product} {product.Name_product} - не найден')

    return redirect(url_for('Admin_products'))



@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product_api(product_id):
    product = Product.query.get_or_404(product_id)

    product_data = {
        'ID_product': product.ID_product,
        'Name_product': product.Name_product,
        'Cost_product': product.Cost_product,
        'IsNew_product': product.IsNew_product,
        'id_master': product.id_master,
        'id_category': product.id_category,

    }

    return jsonify(product_data)



# Route to change Product
@app.route('/admin/edit_product', methods=['GET', 'POST'])
def edit_product():
    error_messages = ()

    if request.method == 'POST':
        edit_code = request.form.get('editCode')
        edit_name = request.form.get('editName')
        edit_price = request.form.get('editPrice')
        edit_new_product = request.form.get('editNewProduct') == 'on'
        edit_master = request.form.get('editMaster')
        edit_category = request.form.get('editCategory')
        product = Product.query.get(edit_code)

        print (str(edit_name))
        # Валидация
        if not edit_name or not edit_price:
            error_messages="Заполните все поля!"

        if edit_category == "Выберите категорию" or edit_master == "Выберите мастера из списка":
            error_messages= "Пожалуйста, выберите категорию и мастера!"

        # try:
        #     edit_price = float(edit_price)  # Проверяем, что цена - число
        # except ValueError:
        #     error_messages["priceisint"] = "Цена должна быть числом!"
        #     return redirect(url_for('AP_add_product')) # Передаем ошибки


        if product:
            #Сохраняем данные
            product.Name_product = edit_name
            product.Cost_product = edit_price
            product.IsNew_product = edit_new_product
            product.id_master = edit_master
            product.id_category = edit_category
        else:
            print (f'Внутренняя ошибка сервера. Продукт {product.ID_product} {product.Name_product} - не найден')
            error_messages = "Продукт не найден"


        if  error_messages:
           flash(error_messages, 'error2')
           return redirect(url_for('Admin_products'))
        else:
            db.session.commit()
            flash("Изменения выполнены успешно!", "error2")
            print(f'Продукт {product.ID_product} - {product.Name_product} успешно изменен')
            return redirect(url_for('Admin_products')) # успешный редирект
    return redirect(url_for('Admin_products'))


#---------AP - Users ---------
@app.route('/admin/users')
def Admin_users():
    users = Users.query.all()
    errors2=get_flashed_messages(category_filter=['error2'])
    if not errors2:
        errors2 = {}
    return render_template('admin/A_users.html', users=users, errors2=errors2)

@app.route('/admin/edit_user', methods=['POST'])
def edit_user():
    error_messages = ""
    if request.method == 'POST':
        edit_code = request.form.get('editCode')
        edit_name = request.form.get('editName')
        edit_phone = request.form.get('editPhone')
        edit_email = request.form.get('editEmail')
        edit_bday = request.form.get('editBday')

        user = Users.query.get(edit_code)

        if not edit_name or not edit_phone or not edit_email:
            error_messages = "Заполните все поля!"

        if user:
           user.Name_user = edit_name
           user.phone_number = edit_phone
           user.mail_user = edit_email

           if edit_bday:
               user.BirthDay_user = datetime.strptime(edit_bday,'%Y-%m-%d').date()
           else:
               user.BirthDay_user = None
        else:
            print(f'Внутренняя ошибка сервера. Пользователь {user.ID_user} - не найден')
            error_messages = "Пользователь не найден"

        if error_messages:
            flash(error_messages, 'error2')
            return redirect(url_for('Admin_users'))
        else:
            db.session.commit()
            flash("Изменения выполнены успешно", 'error2')
            print(f'Пользователь {user.ID_user} - {user.Name_user} успешно изменен')
            return redirect(url_for('Admin_users'))


@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user_api(user_id):
    user = Users.query.get_or_404(user_id)

    user_data = {
        'ID_user': user.ID_user,
        'Name_user': user.Name_user,
        'phone_number': user.phone_number,
        'mail_user': user.mail_user,
        'BirthDay_user': user.BirthDay_user.isoformat() if user.BirthDay_user else None,
        'created_at': user.created_at.isoformat()

    }

    return jsonify(user_data)

@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    user= Users.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        print (f'Пользователь {user.ID_user} - {user.Name_user} успешно удален')
    else:
        print (f'Внутренняя ошибка сервера. Пользователь {user.ID_user} - не найден')

    return redirect(url_for('Admin_users'))

#---------AP - Category ---------
# Route to add category
@app.route('/admin/add_category', methods=['POST'])
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        if not name:
            flash("Наименование категории обязательно для заполнения!", 'error1')
            return redirect(url_for('Admin_categories'))

        new_category = Categories(
            Name_category=name,
            Discription_category=description
        )
        db.session.add(new_category)
        db.session.commit()

        flash("Категория успешно добавлена!", 'success')
        return redirect(url_for('Admin_categories'))
    return render_template('admin/categories_admin.html')



# Route to delete category
@app.route('/delete_category/<int:id>', methods=['POST'])
def delete_category(id):
    category = Categories.query.get(id)
    if category:
        db.session.delete(category)
        db.session.commit()
        print(f'Категория {category.ID_categories} - {category.Name_category} успешно удалена')
    else:
        print(f'Внутренняя ошибка сервера. Категория не найдена')

    return redirect(url_for('Admin_categories'))


# Route to api get category
@app.route('/api/category/<int:category_id>', methods=['GET'])
def get_category_api(category_id):
    category = Categories.query.get_or_404(category_id)

    category_data = {
        'ID_categories': category.ID_categories,
        'Name_category': category.Name_category,
        'Discription_category': category.Discription_category
    }

    return jsonify(category_data)

# Route to edit category
@app.route('/admin/edit_category', methods=['GET','POST'])
def edit_category():
    error_messages = ()

    if request.method == 'POST':
         edit_code = request.form.get('editCode')
         edit_name = request.form.get('editName')
         edit_description = request.form.get('editDescription')
         category = Categories.query.get(edit_code)

         if not edit_name:
             error_messages = "Заполните все обязательные поля"


         if category:
            category.Name_category = edit_name
            category.Discription_category = edit_description
         else:
            print(f'Внутренняя ошибка сервера. Категория {category.ID_categories} - не найдена')
            error_messages = "Категория не найдена"


         if error_messages:
            flash(error_messages, 'error2')
            return redirect(url_for('Admin_categories'))
         else:
            db.session.commit()
            flash("Изменения выполнены успешно!", 'error2')
            print(f'Категория {category.ID_categories} - {category.Name_category} успешно изменена')
            return redirect(url_for('Admin_categories'))

# new route for categories page
@app.route('/admin/categories')
def Admin_categories():
    categories = Categories.query.all()
    errors1=get_flashed_messages(category_filter=['error1'])
    if not errors1:
        errors1 = {}
    errors2=get_flashed_messages(category_filter=['error2'])
    if not errors2:
        errors2 = {}
    return render_template('admin/categories_admin.html', categories=categories, errors1=errors1, errors2=errors2)

# АВТОРИЗАЦИЯ \ РЕГИСТРАЦИЯ
@app.route('/signup') # Вывод страницы авторизации \ регистрации
def signup():
    return render_template('reg.html', errors={})

# Кнопка зарегистрироваться
@app.route('/registration', methods=["POST"])
def registration():
    nick_name = request.form.get('full_nameSign')
    phone = request.form.get('phone')
    password = request.form.get('passwordSign')
    confirm_password = request.form.get('confirm_passwordSign')
    email = request.form.get('emailSign')

    #проверки
    error_messages = {}
    if not nick_name or not phone or not password or not email:
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


    new_user = Users(
        Name_user=nick_name,
        phone_number=phone,
        hash_user=generate_password_hash(password),
        mail_user=email,
    )
    db.session.add(new_user)
    db.session.commit()

    flash("Регистрация прошла успешно! Теперь вы можете войти.", "success")
    return redirect('/signup')

    # return render_template('reg.html')


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        data = request.get_json()

        product_id = data.get('id')
        product_name = data.get('name')
        product_price = data.get('price')

        if 'cart' not in session:
            session['cart'] = []

        session['cart'].append({
            'id': product_id,
            'name': product_name,
            'price': product_price
        })

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
