from flask import Flask, render_template,url_for, send_file,redirect, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import io
from flask_login import LoginManager, current_user
from models import Users, Product, db
from flask_cors import CORS
from flask_migrate import Migrate
import os
import logging
import json
from dotenv import load_dotenv


load_dotenv()
APP_PORT = os.getenv('APP_PORT')
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
CORS(app, origins="http://localhost:3000", supports_credentials=True, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///woodyDB.db')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-dev-key')
db.init_app(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.signup'


# Чтение asset-manifest.json для React
def load_manifest():
    manifest_path = os.path.join(app.static_folder, 'catalog/asset-manifest.json')
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        return manifest
    return {}

manifest = load_manifest()

# Контекстный процессор для доступа к entrypoints React
@app.context_processor
def utility_processor():
    def get_entrypoints():
        return manifest.get('entrypoints', [])
    return dict(get_entrypoints=get_entrypoints)

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
from api import api_bp
from seller import seller_bp
from catalog import catalog_bp

app.register_blueprint(handler_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)
app.register_blueprint(seller_bp)
app.register_blueprint(catalog_bp)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/', methods = ['GET'])
def index():


    productNew = Product.query.filter_by(IsNew_product=1).all()
    return render_template('main.html', productNew=productNew, username=session.get('user_name')) #user_name рудимент?

@app.context_processor
def inject_avatar():
    avatar_url = url_for('static', filename='image/default_avatar.png')
    if current_user.is_authenticated:
        if current_user.avatar:
            avatar_url = url_for('api.get_avatar', user_id=current_user.ID_user)
    return dict(avatar_url=avatar_url)

@app.route('/base')
def showBase():
    return render_template('base.html', username=session.get('user_name'))


if __name__ == "__main__":
    app.run(host="localhost", port=APP_PORT, debug=True)
