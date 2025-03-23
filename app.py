from flask import Flask, render_template,url_for, send_file,redirect, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import io
from flask_login import LoginManager, UserMixin, current_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///woodyDB.db'
app.secret_key = '1111'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.signup'




#обработка ошибок
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403

# Функция для установки заголовков кэширования
def set_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# заголовки кэширования после каждого запроса
@app.after_request
def add_header(response):
    return set_cache_headers(response)



# DB Models
class Genders(db.Model):
    __tablename__ = 'Genders'
    ID_gender = db.Column(db.Integer, primary_key=True)
    gender_name = db.Column(db.String, nullable=False)
    short_name = db.Column(db.String)

class Users(UserMixin, db.Model):
    __tablename__ = 'Users'
    ID_user = db.Column(db.Integer, primary_key=True)
    Name_user = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String)
    hash_user = db.Column(db.String, nullable=False)
    mail_user = db.Column(db.String, nullable=False, unique=True)
    BirthDay_user = db.Column(db.Date)
    id_gender = db.Column(db.Integer, db.ForeignKey('Genders.ID_gender'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    role = db.Column(db.String, default='user')
    avatar = db.Column(db.LargeBinary, nullable=True)


    gender = db.relationship('Genders', backref='users')

    def get_id(self): # fix UserMixin
        return (str(self.ID_user))

    def is_admin(self):
        return self.role == 'admin'

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


# Импорт и регистрация blueprints (модулей)
from auth import auth_bp
from admin import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)


#Routes
@app.route('/product_image/<int:product_id>')
def product_image(product_id):
    product = Product.query.get_or_404(product_id)
    return send_file(io.BytesIO(product.image_product), mimetype='image/jpeg')

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id) # возможно нужно обвернуть в int

@app.route('/product/<int:product_id>')
def productCard(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)



@app.route('/', methods = ['GET'])
def index():


    productNew = Product.query.filter_by(IsNew_product=1).all()
    return render_template('main.html', productNew=productNew, username=session.get('user_name')) #user_name рудимент?

@app.route('/get_avatar/<int:user_id>') # предоставление Аватара
def get_avatar(user_id):
    user = Users.query.get_or_404(user_id)

    if user.avatar:
        return send_file(io.BytesIO(user.avatar), mimetype='image/*') #что по расшерениям другим?
    else:
        return redirect(url_for('static', filename='image/default_avatar.png'))

@app.context_processor
def inject_avatar():
    avatar_url = url_for('static', filename='image/default_avatar.png')
    if current_user.is_authenticated:
        if current_user.avatar:
            avatar_url = url_for('get_avatar', user_id=current_user.ID_user)
    return dict(avatar_url=avatar_url)

@app.route('/base')
def showBase():
    return render_template('base.html', username=session.get('user_name'))




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
