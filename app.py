from flask import Flask, render_template,url_for, send_file,redirect, request, jsonify, session,flash
from flask_sqlalchemy import SQLAlchemy
import io
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
