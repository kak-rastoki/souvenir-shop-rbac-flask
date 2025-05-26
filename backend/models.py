"""
Модели таблиц из Базы данных
--------------------------------------------------
Описание:

"""

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

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

class OrderStatus:
    CART = 'неактивен'
    PENDING = 'активен'
    COMPLETED = 'завершен'
    CANCELLED = 'отменен'

class Order(db.Model):
    __tablename__ = 'Order'
    ID_order = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('Users.ID_user'))
    Data_order = db.Column(db.DateTime, default=func.now())
    Status_order = db.Column(db.String(50), default=OrderStatus.CART, nullable=False)

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
