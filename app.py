from flask import Flask, render_template,url_for, send_file,redirect, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import io
from flask_login import LoginManager, current_user
from models import Users, Product, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///woodyDB.db'
app.secret_key = '1111'
# db = SQLAlchemy(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.signup'


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


# Импорт и регистрация blueprints (модулей)
from auth import auth_bp
from admin import admin_bp
from handler import handler_bp

app.register_blueprint(handler_bp)
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
