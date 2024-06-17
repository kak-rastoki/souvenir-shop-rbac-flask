from flask import Flask, render_template,send_file, request
from flask_sqlalchemy import SQLAlchemy
import io

#configs
app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///woodyDB.db'
db = SQLAlchemy(app)


#DB Models----------------------------------------------------------#
class Order(db.Model): # таблица заказов объединяющая все таблички

    ID_order = db.Column(db.Integer,primary_key=True)
    id_user =db.Column(db.Integer, db.ForeignKey('User.id'), nullable = False )
    id_product = db.Column(db.Integer, nullable = False)
    id_master = db.Column(db.Integer, nullable = False)
    data_order = db.Column(db.String(50), nullable = False)
    status_order = db.Column(db.Boolean, nullable = False) # active \ unactive


class Categories(db.Model): #категории товаров и их описание \\

    ID_categories = db.Column (db.Integer,primary_key=True)
    Name_categories = db.Column(db.String(50),nullable = False)
    Discription_categories = db.Column(db.String(100))


class Product(db.Model):
    ID_product = db.Column(db.Integer, primary_key=True)
    Name_product = db.Column(db.String, nullable=False, unique=True)
    Cost_product = db.Column(db.Integer, nullable=False)
    Description_product = db.Column(db.String)
    Id_category = db.Column(db.Integer, nullable=False)
    isNew_product = db.Column(db.Integer, nullable=False)
    image_product = db.Column (db.LargeBinary, nullable = True)
#-------------------------------------------------------------------#


#Routes-------------------------------------------------------------#
@app.route('/product_image/<int:product_id>')
def product_image(product_id):
    product = Product.query.get_or_404(product_id)
    return send_file(io.BytesIO(product.image_product), mimetype="image/jpeg")

@app.route('/signup')
def signup():
    return render_template ('reg.html')

#странциа продукта
@app.route('/product/<int:product_id>')
def productCard(product_id,):
    product = Product.query.get_or_404(product_id)


    return render_template ('product.html',product=product)


@app.route ('/')
def index():
    productNew = Product.query.filter_by(isNew_product=1).all()
    return render_template('main.html', productNew = productNew)


@app.route ('/base')
def showBase():

    return render_template('base.html')



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000,debug=True)
# почему-то порт не переназначается5
