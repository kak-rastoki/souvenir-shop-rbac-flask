import io
from flask import send_file, render_template, redirect, url_for
from api import api_bp
from models import Product, Users


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
