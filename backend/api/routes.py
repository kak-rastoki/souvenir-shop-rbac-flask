import io
from flask import send_file, render_template, redirect, url_for, jsonify, request
from api import api_bp
from models import Product, Users, Categories, Order, OrderProduct, Currency, db
import base64
from sqlalchemy import desc
from flask_login import login_required, current_user
from decorators import custom_login_required

# Получить содержимое корзины
@api_bp.route('/api/cart', methods=['GET'])
@login_required
def get_cart():

    cart = Order.query.filter_by(id_user=current_user.ID_user, Status_order=False).first()
    if not cart:
        cart = Order(id_user=current_user.ID_user, Status_order=False, Data_order=db.func.current_date())
        db.session.add(cart)
        db.session.commit()

    items = [
        {
            'id': item.ID_OP,
            'product_id': item.id_product,
            'name': item.product.Name_product,
            'price': item.product.Cost_product,
            'quantity': item.quantity,
            'image': base64.b64encode(item.product.image_product).decode('utf-8') if item.product.image_product else None,
            'total': item.product.Cost_product * item.quantity
        }
        for item in cart.order_products
    ]
    total_price = sum(item['total'] for item in items)
    return jsonify({'items': items, 'total_price': total_price})

# Добавить товар в корзину
@custom_login_required
@api_bp.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    print(f"Current user: {current_user.ID_user if current_user.is_authenticated else 'Not authenticated'}")
    print(f"Cookies in request: {request.cookies.get('session')}")

    print("текущий пользователь: ", current_user)
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    product = Product.query.get_or_404(product_id)
    cart = Order.query.filter_by(id_user=current_user.ID_user, Status_order=False).first()
    if not cart:
        cart = Order(id_user=current_user.ID_user, Status_order=False, Data_order=db.func.current_date())
        db.session.add(cart)
        db.session.commit()

    # Проверяем, есть ли товар уже в корзине
    cart_item = OrderProduct.query.filter_by(id_order=cart.ID_order, id_product=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = OrderProduct(
            id_order=cart.ID_order,
            id_product=product_id,
            quantity=quantity,
            id_currency=1
        )
        db.session.add(cart_item)

    db.session.commit()
    return jsonify({'message': 'Товар добавлен в корзину'})

# Обновить количество товара
@api_bp.route('/api/cart/update/<int:product_id>', methods=['PUT'])
@login_required
def update_cart_item(product_id):
    data = request.get_json()
    quantity = data.get('quantity')

    cart = Order.query.filter_by(id_user=current_user.ID_user, Status_order=False).first_or_404()
    cart_item = OrderProduct.query.filter_by(id_order=cart.ID_order, id_product=product_id).first()
    if not cart_item:
        return jsonify({'error': 'Товар не найден в корзине'}), 404

    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity

    db.session.commit()
    return jsonify({'message': 'Количество обновлено'})

# Удалить товар из корзины
@api_bp.route('/api/cart/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_cart(product_id):
    cart = Order.query.filter_by(id_user=current_user.ID_user, Status_order=False).first_or_404()
    cart_item = OrderProduct.query.filter_by(id_order=cart.ID_order, id_product=product_id).first()
    if not cart_item:
        return jsonify({'error': 'Товар не найден в корзине'}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Товар удалён из корзины'})

# Очистить корзину
@api_bp.route('/api/cart/clear', methods=['DELETE'])
@login_required
def clear_cart():
    cart = Order.query.filter_by(id_user=current_user.ID_user, Status_order=False).first_or_404()
    OrderProduct.query.filter_by(id_order=cart.ID_order).delete()
    db.session.commit()
    return jsonify({'message': 'Корзина очищена'})

# Оформить заказ
@api_bp.route('/api/cart/checkout', methods=['POST'])
@custom_login_required
def checkout():
    cart = Order.query.filter_by(id_user=current_user.ID_user, Status_order=False).first_or_404()
    if not cart.order_products:
        return jsonify({'error': 'Корзина пуста'}), 400
    print (cart.ID_order);
    cart.Status_order = True
    cart.Data_order = db.func.current_date()
    db.session.commit()
    return jsonify({
        'message': 'Заказ оформлен',
        'order_id': cart.ID_order
        })


@api_bp.route('/api/product/<int:product_id>')
def get_product_by_id(product_id):
    product = Product.query.filter_by(ID_product=product_id).first_or_404()

    return jsonify({
        'id': product.ID_product,
        'name': product.Name_product,
        'cost': product.Cost_product,
        'discription': product.Description_product,
        'category': product.category.Name_category,
        'master': product.master.Name_master,
        'image': base64.b64encode(product.image_product).decode('utf-8') if product.image_product else None
    })

@api_bp.route('/api/products_by_category', methods=['POST'])
def product_by_category():
    data = request.get_json()
    category = data['category']
    if not data or 'category' not in data:
        return jsonify({'error': 'Category name is required'}), 400
    price_filter = data.get('priceFilter', {})
    min_price = price_filter.get('minPrice', None)
    max_price = price_filter.get('maxPrice', None)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    sort = request.args.get('sort', 'desc', type=str)

    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 12

    query = Product.query.filter(Product.category.has(Name_category=category))

    conditions = []
    if max_price:
        conditions.append(Product.Cost_product <= float(max_price))
    if min_price:
        conditions.append(Product.Cost_product >= float(min_price))
    if conditions:
        query = query.filter(*conditions)

    if not query.count() and not Categories.query.filter_by(Name_category=category).first():
        return jsonify({
            'products': [],
            'current_page': 1,
            'total_pages': 0,
            'error': f'Category "{category}" not found'
        }), 404

    if sort.lower() == 'desc':
        query = query.order_by(desc(Product.Cost_product))
    else:
        query = query.order_by(Product.Cost_product)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    products = pagination.items
    total_pages = pagination.pages
    current_page = pagination.page

    product_list = []
    for product in products:
        product_dict = {
            'id': product.ID_product,
            'name': product.Name_product,
            'price': product.Cost_product,
            'image': base64.b64encode(product.image_product).decode('utf-8') if product.image_product else None
        }
        product_list.append(product_dict)

    return jsonify({
        'products': product_list,
        'current_page': current_page,
        'total_pages': total_pages,
        'minPrice': min_price,
        'maxPrice': max_price,
        'sort': sort
    })

@api_bp.route('/api/product_page/<int:product_id>')
def productCard(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@api_bp.route('/product_image/<int:product_id>')
def product_image(product_id):
    product = Product.query.get_or_404(product_id)
    return send_file(io.BytesIO(product.image_product), mimetype='image/jpeg')

@api_bp.route('/get_avatar/<int:user_id>')
def get_avatar(user_id):
    user = Users.query.get_or_404(user_id)
    if user.avatar:
        return send_file(io.BytesIO(user.avatar), mimetype='image/*')
    else:
        return redirect(url_for('static', filename='image/default_avatar.png'))
