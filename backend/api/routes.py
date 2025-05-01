import io
from flask import send_file, render_template, redirect, url_for,jsonify, request
from api import api_bp
from models import Product, Users
import base64


# @api_bp.route('/api/products') #для разработки фронта
# def get_products():
#     products = [
#         { 'id': 1, 'name': 'Статуетка медведя', 'price': 1832, 'image_url': './static/image/Beer1.png', 'category': "сувениры"},
#         { 'id': 2, 'name': 'Картина из дерева "Дрож"', 'price': 4353, 'image_url': './static/image/Beer1.png', 'category': "картины"},
#         { 'id': 3, 'name': 'Картина из дерева', 'price': 3453, 'image_url': '/static/image/Beer1.png', 'category': "сувениры"},
#         { 'id': 4, 'name': 'Статуетка медведя', 'price': 176, 'image_url': '/static/image/Beer1.png', 'category': "сувениры"},
#         { 'id': 5, 'name': 'Статуетка медведя', 'price': 1353, 'image_url': '/static/image/Beer1.png', 'category': "сувениры"},
#         { 'id': 6, 'name': 'Статуетка медведя', 'price': 153, 'image_url': '/static/image/Beer1.png', 'category': "сувениры"},
#         { 'id': 7, 'name': 'Статуетка медведя', 'price': 256, 'image_url': '/static/image/Beer1.png', 'category': "сувениры"},
#     ]
#     return jsonify(products)


@api_bp.route('/api/products_by_category', methods = ['POST']) # Получение товаров по категории, которая прилетит с фронта
def product_by_category():
    data = request.get_json()
    category = data.get('category')
    products = Product.query.filter(Product.category.has(Name_category=category)).all()

    if not category:
        return jsonify({'error': 'Category name is required'}), 400

    product_list = [{
        'id': product.ID_product,
        'name': product.Name_product,
        'price': product.Cost_product,
        'image': base64.b64encode(product.image_product).decode('utf-8') if product.image_product else None

        } for product in products]

    return jsonify ({'products' : product_list})

@api_bp.route('/product/<int:product_id>') # Получение товара
def productCard(product_id):
    product = Product.query.get_or_404(product_id)

    return render_template('product.html', product=product)



@api_bp.route('/product_image/<int:product_id>') # Получение изображения товара
def product_image(product_id):
    product = Product.query.get_or_404(product_id)
    return send_file(io.BytesIO(product.image_product), mimetype='image/jpeg')


@api_bp.route('/get_avatar/<int:user_id>') # предоставление Аватара
def get_avatar(user_id):
    user = Users.query.get_or_404(user_id)

    if user.avatar:
        return send_file(io.BytesIO(user.avatar), mimetype='image/*') #что по расшерениям другим?
    else:
        return redirect(url_for('static', filename='image/default_avatar.png'))
