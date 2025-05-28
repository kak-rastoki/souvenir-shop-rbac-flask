from . import seller_bp
from flask_login import login_required, current_user
from datetime import datetime
import base64
from flask import render_template,url_for, redirect, request, jsonify, get_flashed_messages,flash,current_app
from decorators import admin_required,seller_required
from models import db, Users, Masters, Categories, Product, Genders, Order, OrderProduct, Review, OrderStatus, Currency
from sqlalchemy import func
import base64
from PIL import Image
import io

THUMBNAIL_SIZE = 50

@seller_bp.route('/seller')
@login_required
@seller_required
def show_dashboard():
  return redirect(url_for('seller.dashboard'))


@seller_bp.route('/seller/bAsE')
@login_required
@seller_required
def show_base():
  return render_template('sellerbase.html')


@seller_bp.route('/seller/dashboard')
@login_required
@seller_required
def dashboard():
    print("сработал дашборд маршрут")
    total_products = Product.query.count()
    total_orders = Order.query.count()
    completed_orders_count = Order.query.filter_by(Status_order="завершен").count()
    pending_orders_count = Order.query.filter_by(Status_order="активен").count()
    cart_orders_count = Order.query.filter_by(Status_order="неактивен").count()


    latest_orders = Order.query.order_by(Order.Data_order.desc()).limit(5).all()


    return render_template('dashboard.html',
                            total_products=total_products,
                            total_orders=total_orders,
                            completed_orders_count=completed_orders_count,
                            pending_orders_count=pending_orders_count,
                            cart_orders_count=cart_orders_count,
                            latest_orders=latest_orders,
                            current_user=current_user
                          )

# Маршрут для отображения списка товаров
@seller_bp.route('/seller/products')
@login_required
@seller_required
def products():
    masters = Masters.query.all()
    categories = Categories.query.all()
    products = Product.query.all() # Получаем все товары

    products_data = []
    for product in products:
        category = Categories.query.get(product.id_category)
        master = Masters.query.get(product.id_master)

        # Обработка изображения для миниатюры
        image_thumbnail_b64 = None # Переименовано обратно на image_thumbnail_b64
        if product.image_product:
            try:
                img = Image.open(io.BytesIO(product.image_product))

                # --- НОВАЯ ЛОГИКА ДЛЯ КВАДРАТНОЙ МИНИАТЮРЫ ---
                # Определяем размеры изображения
                width, height = img.size

                # Определяем меньшую сторону
                min_dim = min(width, height)

                # Вычисляем координаты для центрального квадратного обрезания
                left = (width - min_dim) / 2
                top = (height - min_dim) / 2
                right = (width + min_dim) / 2
                bottom = (height + min_dim) / 2

                # Обрезаем изображение до квадрата
                img = img.crop((left, top, right, bottom))

                # Изменяем размер обрезанного изображения до нужного размера миниатюры
                # Используем Image.Resampling.LANCZOS для лучшего качества при уменьшении
                img = img.resize((THUMBNAIL_SIZE, THUMBNAIL_SIZE), Image.Resampling.LANCZOS)
                # --- КОНЕЦ НОВОЙ ЛОГИКИ ---

                # Сохраняем миниатюру в байтовый поток
                byte_arr = io.BytesIO()
                # Для прозрачности лучше PNG, если нужна оптимизация размера - JPEG (но без прозрачности)
                img.save(byte_arr, format='PNG')
                # Кодируем в Base64
                image_thumbnail_b64 = base64.b64encode(byte_arr.getvalue()).decode('utf-8')
            except Exception as e:
                current_app.logger.error(f"Ошибка обработки изображения для товара {product.ID_product}: {e}")
                image_thumbnail_b64 = None

        products_data.append({
            'ID_product': product.ID_product,
            'Name_product': product.Name_product,
            'Cost_product': product.Cost_product,
            'Description_product': product.Description_product,
            'Category_name': category.Name_category if category else 'Неизвестно',
            'Master_name': master.Name_master if master else 'Неизвестно',
            'IsNew_product': product.IsNew_product,
            'id_master': product.id_master, # Передаем ID для форм
            'id_category': product.id_category, # Передаем ID для форм
            'image_thumbnail_b64': image_thumbnail_b64 # Миниатюра в Base64
        })


    errors = get_flashed_messages(category_filter=['error'])
    success_messages = get_flashed_messages(category_filter=['success'])

    return render_template('seller/products.html',
                           masters=masters,
                           categories=categories,
                           products=products_data,
                           errors=errors, # Передаем все ошибки
                           success_messages=success_messages)

# Вспомогательная функция для проверки разрешенных расширений файла
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# Получение товара
@seller_bp.route('/seller/product_data/<int:product_id>', methods=['GET']) # <--- ИЗМЕНЕНО ЗДЕСЬ
@login_required
@seller_required
def get_product_data_for_edit(product_id): # <--- ИЗМЕНЕНО ИМЯ ФУНКЦИИ ДЛЯ ЯСНОСТИ
    product = Product.query.get_or_404(product_id)

    product_data = {
        'ID_product': product.ID_product,
        'Name_product': product.Name_product,
        'Cost_product': product.Cost_product,
        'Description_product': product.Description_product,
        'IsNew_product': product.IsNew_product,
        'id_master': product.id_master,
        'id_category': product.id_category,
    }
    return jsonify(product_data)

# РедактированиЕ товара
@seller_bp.route('/seller/products/edit', methods=['POST'])
@login_required
@seller_required
def edit_product():
    if request.method == 'POST':
        edit_code = request.form.get('editCode')
        edit_name = request.form.get('editName')
        edit_price = request.form.get('editPrice')
        edit_new_product = request.form.get('editNewProduct') == 'on'
        edit_master_id = request.form.get('editMaster')
        edit_category_id = request.form.get('editCategory')
        edit_description = request.form.get('editDescription')
        edit_file = request.files.get('editFile')

        product = Product.query.get(edit_code)

        if not product:
            flash("Ошибка: Товар для редактирования не найден.", "error")
            return redirect(url_for('seller.products'))


        if not edit_name or not edit_price or not edit_master_id or not edit_category_id:
            flash("Все поля (кроме описания и изображения) обязательны для заполнения!", "error")
            return redirect(url_for('seller.products'))

        if edit_category_id == "Выберите категорию" or edit_master_id == "Выберите мастера из списка":
            flash("Пожалуйста, выберите категорию и мастера!", "error")
            return redirect(url_for('seller.products'))

        try:
            edit_price = float(edit_price)
            if edit_price <= 0:
                flash("Цена должна быть положительным числом!", "error")
                return redirect(url_for('seller.products'))
        except ValueError:
            flash("Цена должна быть числом!", "error")
            return redirect(url_for('seller.products'))


        product.Name_product = edit_name
        product.Cost_product = edit_price
        product.Description_product = edit_description
        product.IsNew_product = edit_new_product
        product.id_master = edit_master_id
        product.id_category = edit_category_id

        # --- КОРРЕКЦИЯ ЛОГИКИ ОБРАБОТКИ ИЗОБРАЖЕНИЯ ---
        if edit_file and edit_file.filename != '':
            # Если файл загружен, проверю его тип и сохраняем
            if allowed_file(edit_file.filename):
                product.image_product = edit_file.read()
            else:
                flash("Недопустимый тип файла изображения. Разрешены: png, jpg, jpeg, gif.", "error")
                return redirect(url_for('seller.products'))
        # else:
            # Если файл не загружен (edit_file пуст), то product.image_product остается без изменений.
            # Благодаря триггеру, если до этого изображение было null, оно уже было заполнено дефолтом.
            # Если оно было пользовательски,то конеч оно сохранится.
        # --- КОНЕЦ КОРРЕКЦИИ ---

        db.session.commit()
        flash("Изменения товара выполнены успешно!", "success")
        return redirect(url_for('seller.products'))

# Удаление товара
@seller_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@login_required
@seller_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        flash(f'Продукт "{product.Name_product}" успешно удален.', 'success')
    else:
        flash(f'Ошибка: Продукт с ID {product_id} не найден.', 'error')
    return redirect(url_for('seller.products'))


# Маршрут для добавления товара
@seller_bp.route('/seller/products/add', methods=['POST'])
@login_required
@seller_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        new_product = request.form.get('newProduct') == 'on'
        master_id = request.form.get('master')
        category_id = request.form.get('category')
        description = request.form.get('description')
        file = request.files.get('file')

        # Валидация (без изменений)
        if not name or not price or not master_id or not category_id:
            flash("Все поля (кроме описания и изображения) обязательны для заполнения!", "error")
            return redirect(url_for('seller.products'))

        if category_id == "" or master_id == "": # Изменено "" вместо "Выберите..."
            flash("Пожалуйста, выберите категорию и мастера!", "error")
            return redirect(url_for('seller.products'))

        try:
            price = float(price)
            if price <= 0:
                flash("Цена должна быть положительным числом!", "error")
                return redirect(url_for('seller.products'))
        except ValueError:
            flash("Цена должна быть числом!", "error")
            return redirect(url_for('seller.products'))

        image_data = None
        if file and file.filename != '':
            if allowed_file(file.filename):
                image_data = file.read()
            else:
                flash("Недопустимый тип файла изображения. Разрешены: png, jpg, jpeg, gif.", "error")
                return redirect(url_for('seller.products'))

        new_product_entry = Product(
            Name_product=name,
            Cost_product=price,
            Description_product=description,
            IsNew_product=new_product,
            id_master=master_id,
            id_category=category_id,
            image_product = image_data
        )
        db.session.add(new_product_entry)
        db.session.commit()

        flash("Товар успешно добавлен!", "success")
        return redirect(url_for('seller.products'))

# детали
@seller_bp.route('/seller/products/<int:product_id>')
@login_required
@seller_required
def view_product_details(product_id):
    product = Product.query.options(
        db.joinedload(Product.category),
        db.joinedload(Product.master).joinedload(Masters.gender) # Загружаем и пол мастера
    ).get_or_404(product_id)

    # Преобразуем изображение в base64 для отображения
    image_b64 = None
    if product.image_product:
        try:
            # Для детальной страницы можно отправить оригинальное изображение
            # или сгенерировать более крупную версию, если THUMBNAIL_SIZE слишком мал
            # Для простоты, пока отправляем оригинальное (или триггерное дефолтное)
            image_b64 = base64.b64encode(product.image_product).decode('utf-8')
        except Exception as e:
            current_app.logger.error(f"Ошибка кодирования изображения для деталей товара {product.ID_product}: {e}")
            image_b64 = None

    return render_template('seller/product_details.html',
                           product=product,
                           image_b64=image_b64)


# --- ЗАКАЗЫ ---
# --- МАРШРУТЫ ДЛЯ ЗАКАЗОВ ПРОДАВЦА ---

@seller_bp.route('/seller/orders') # ИСПРАВЛЕНО: маршрут теперь /seller/orders
@login_required
@seller_required
def show_orders():
    # Используем db.contains_eager для более эффективной загрузки связанных данных
    # Если Order.user, OrderProduct.product, OrderProduct.currency имеют обратные ссылки (backref)
    # то db.joinedload или db.subqueryload могут быть более подходящими.
    # Для joinedload, добавь его к запросу:
    orders = Order.query.options(
        db.joinedload(Order.user),
        db.joinedload(Order.order_products).joinedload(OrderProduct.product),
        db.joinedload(Order.order_products).joinedload(OrderProduct.currency)
    ).order_by(Order.Data_order.desc()).all()


    orders_data = []
    for order in orders:
        # User:
        user_name = order.user.Name_user if order.user else 'Удаленный пользователь'
        user_mail = order.user.mail_user if order.user else 'N/A'
        phone_number = order.user.phone_number if order.user else 'N/A'

        total_sum = 0
        products_in_order = []
        for op in order.order_products: # Теперь `order.order_products` уже загружен
            # Проверки на None нужны, если связанные объекты могут быть None
            product = op.product
            currency = op.currency

            if product and currency:
                item_price = product.Cost_product * op.quantity
                total_sum += item_price
                products_in_order.append({
                    'ID_product': product.ID_product,
                    'Name_product': product.Name_product,
                    'quantity': op.quantity,
                    'Cost_product': product.Cost_product,
                    'currency_symbol': currency.symbol
                })
            elif product: # Если нет валюты, но есть продукт
                item_price = product.Cost_product * op.quantity
                total_sum += item_price
                products_in_order.append({
                    'ID_product': product.ID_product,
                    'Name_product': product.Name_product,
                    'quantity': op.quantity,
                    'Cost_product': product.Cost_product,
                    'currency_symbol': 'руб.' # Дефолтная валюта
                })

        orders_data.append({
            'ID_order': order.ID_order,
            'user_name': user_name,
            'user_mail': user_mail,
            'phone_number': phone_number,
            'Data_order': order.Data_order.strftime('%Y-%m-%d %H:%M:%S'),
            'Status_order': order.Status_order, # Это уже строковое значение
            'total_sum': total_sum, # ИСПРАВЛЕНО: добавлено total_sum
            'products_in_order': products_in_order,
        })

    available_statuses = ['неактивен', 'активен', 'завершен']

    errors = get_flashed_messages(category_filter=['error'])
    success_messages = get_flashed_messages(category_filter=['success'])

    return render_template('seller/orders.html',
                           orders=orders_data,
                           available_statuses=available_statuses,
                           errors=errors,
                           success_messages=success_messages)

# Маршрут для просмотра деталей заказа (отдельная страница)
@seller_bp.route('/seller/orders/<int:order_id>')
@login_required
@seller_required
def view_order_details(order_id):
    order = Order.query.options(
        db.joinedload(Order.user),
        db.joinedload(Order.order_products).joinedload(OrderProduct.product),
        db.joinedload(Order.order_products).joinedload(OrderProduct.currency)
    ).get_or_404(order_id)

    user = order.user

    total_sum = 0
    products_in_order = []
    for op in order.order_products:
        product = op.product
        currency = op.currency

        if product and currency:
            item_price = product.Cost_product * op.quantity
            total_sum += item_price
            products_in_order.append({
                'ID_product': product.ID_product,
                'Name_product': product.Name_product,
                'quantity': op.quantity,
                'Cost_product': product.Cost_product,
                'currency_symbol': currency.symbol
            })
        elif product: # Если нет валюты, но есть продукт
            item_price = product.Cost_product * op.quantity
            total_sum += item_price
            products_in_order.append({
                'ID_product': product.ID_product,
                'Name_product': product.Name_product,
                'quantity': op.quantity,
                'Cost_product': product.Cost_product,
                'currency_symbol': 'руб.' # Дефолтная валюта
            })


    return render_template('seller/order_details.html',
                           order=order,
                           user=user,
                           products_in_order=products_in_order,
                           total_sum=total_sum)

# Маршрут для изменения статуса заказа
@seller_bp.route('/seller/orders/update_status', methods=['POST'])
@login_required
@seller_required
def update_order_status():
    order_id = request.form.get('order_id')
    new_status = request.form.get('new_status')

    order = Order.query.get(order_id)
    if not order:
        flash("Ошибка: Заказ не найден.", "error")
        return redirect(url_for('seller.show_orders'))

    # Проверка на допустимость статуса
    if new_status not in ['неактивен', 'активен', 'завершен']:
        flash(f"Ошибка: Недопустимый статус '{new_status}'.", "error")
        return redirect(url_for('seller.show_orders'))

    order.Status_order = new_status
    db.session.commit()
    flash(f"Статус заказа #{order_id} успешно изменен на '{new_status}'.", "success")
    return redirect(url_for('seller.show_orders'))

# Маршрут для удаления заказа
@seller_bp.route('/seller/orders/delete/<int:order_id>', methods=['POST'])
@login_required
@admin_required
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        flash(f'Ошибка: Заказ с ID {order_id} не найден.', 'error')
        return redirect(url_for('seller.show_orders'))

    try:
        # Сначала удаляем связанные OrderProduct
        OrderProduct.query.filter_by(id_order=order.ID_order).delete()

        db.session.delete(order)
        db.session.commit()
        flash(f'Заказ #{order_id} успешно удален.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении заказа #{order_id}: {str(e)}', 'error')

    return redirect(url_for('seller.show_orders'))

# ---КАТЕГОРИИ ---

# Маршрут для отображения списка категорий
@seller_bp.route('/seller/categories')
@login_required
@seller_required
def categories():
    categories = Categories.query.all()

    errors = get_flashed_messages(category_filter=['error'])
    success_messages = get_flashed_messages(category_filter=['success'])

    return render_template('seller/categories.html',
                           categories=categories,
                           errors=errors,
                           success_messages=success_messages)

# Маршрут для добавления категории
@seller_bp.route('/seller/categories/add', methods=['POST'])
@login_required
@seller_required
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        if not name:
            flash("Наименование категории обязательно для заполнения!", 'error')
            return redirect(url_for('seller.categories'))

        new_category = Categories(
            Name_category=name,
            Discription_category=description
        )
        db.session.add(new_category)
        db.session.commit()

        flash("Категория успешно добавлена!", 'success')
        return redirect(url_for('seller.categories'))

# Маршрут для получения данных категории по ID (для формы редактирования)
@seller_bp.route('/seller/category_data/<int:category_id>', methods=['GET'])
@login_required
@seller_required
def get_category_data_for_edit(category_id):
    category = Categories.query.get_or_404(category_id)

    category_data = {
        'ID_categories': category.ID_categories,
        'Name_category': category.Name_category,
        'Discription_category': category.Discription_category
    }
    return jsonify(category_data)

# Маршрут для редактирования категории
@seller_bp.route('/seller/categories/edit', methods=['POST'])
@login_required
@seller_required
def edit_category():
    if request.method == 'POST':
        edit_code = request.form.get('editCode')
        edit_name = request.form.get('editName')
        edit_description = request.form.get('editDescription')

        category = Categories.query.get(edit_code)

        if not category:
            flash("Ошибка: Категория для редактирования не найдена.", "error")
            return redirect(url_for('seller.categories'))

        if not edit_name:
            flash("Наименование категории обязательно для заполнения!", 'error')
            return redirect(url_for('seller.categories'))

        category.Name_category = edit_name
        category.Discription_category = edit_description

        db.session.commit()
        flash("Изменения категории выполнены успешно!", "success")
        return redirect(url_for('seller.categories'))

# Маршрут для удаления категории
@seller_bp.route('/seller/categories/delete/<int:category_id>', methods=['POST'])
@login_required
@seller_required
def delete_category(category_id):
    category = Categories.query.get(category_id)
    if not category:
        flash(f'Ошибка: Категория с ID {category_id} не найдена.', 'error')
        return redirect(url_for('seller.categories'))

    try:
        # Проверка наличия связанных товаров (если ON DELETE CASCADE не настроен в БД)
        # Если есть связанные товары, сначала нужно их обнулить или удалить,
        # иначе возникнет IntegrityError.
        db.session.delete(category)
        db.session.commit()
        flash(f'Категория "{category.Name_category}" успешно удалена.', 'success')
    except Exception as e:
        db.session.rollback()
        # Если произошла ошибка из-за связанных данных (например, IntegrityError),
        # то можно добавить более конкретное сообщение
        if "FOREIGN KEY constraint failed" in str(e):
             flash(f'Невозможно удалить категорию "{category.Name_category}", так как существуют связанные товары.', 'error')
        else:
            flash(f'Ошибка при удалении категории "{category.Name_category}": {str(e)}', 'error')

    return redirect(url_for('seller.categories'))


# --- МАСТЕРА ---
# Маршрут для отображения списка мастеров
@seller_bp.route('/seller/masters')
@login_required
@seller_required
def masters():
    masters = Masters.query.options(db.joinedload(Masters.gender)).all()

    masters_data = []
    for master in masters:
        masters_data.append({
            'ID_master': master.ID_master,
            'Name_master': master.Name_master,
            'id_gender': master.id_gender,
            'gender_name': master.gender.gender_name if master.gender else 'Неизвестно'
        })

    errors = get_flashed_messages(category_filter=['error'])
    success_messages = get_flashed_messages(category_filter=['success'])
    genders = Genders.query.all() # Для формы добавления/редактирования

    return render_template('seller/masters.html',
                           masters=masters_data,
                           genders=genders,
                           errors=errors,
                           success_messages=success_messages)

# Маршрут для добавления мастера
@seller_bp.route('/seller/masters/add', methods=['POST'])
@login_required
@seller_required
def add_master():
    if request.method == 'POST':
        name = request.form.get('name')
        gender_id = request.form.get('gender')

        if not name:
            flash("Наименование мастера обязательно для заполнения!", 'error')
            return redirect(url_for('seller.masters'))

        if not gender_id or gender_id == "": # Проверка, что пол выбран
            flash("Выберите пол мастера!", 'error')
            return redirect(url_for('seller.masters'))

        new_master = Masters(
            Name_master=name,
            id_gender=gender_id,
        )
        db.session.add(new_master)
        db.session.commit()

        flash("Мастер успешно добавлен!", 'success')
        return redirect(url_for('seller.masters'))

# Маршрут для получения данных мастера по ID (для формы редактирования)
@seller_bp.route('/seller/master_data/<int:master_id>', methods=['GET'])
@login_required
@seller_required
def get_master_data_for_edit(master_id):
    master = Masters.query.get_or_404(master_id)

    master_data = {
        'ID_master': master.ID_master,
        'Name_master': master.Name_master,
        'id_gender': master.id_gender
    }
    return jsonify(master_data)

# Маршрут для редактирования мастера
@seller_bp.route('/seller/masters/edit', methods=['POST'])
@login_required
@seller_required
def edit_master():
    if request.method == 'POST':
        edit_code = request.form.get('editCode')
        edit_name = request.form.get('editName')
        edit_gender_id = request.form.get('editGender')

        master = Masters.query.get(edit_code)

        if not master:
            flash("Ошибка: Мастер для редактирования не найден.", "error")
            return redirect(url_for('seller.masters'))

        if not edit_name:
            flash("Наименование мастера обязательно для заполнения!", 'error')
            return redirect(url_for('seller.masters'))

        if not edit_gender_id or edit_gender_id == "": # Проверка, что пол выбран
            flash("Выберите пол мастера!", 'error')
            return redirect(url_for('seller.masters'))

        master.Name_master = edit_name
        master.id_gender = edit_gender_id

        db.session.commit()
        flash("Изменения мастера выполнены успешно!", "success")
        return redirect(url_for('seller.masters'))

# Маршрут для удаления мастера
@seller_bp.route('/seller/masters/delete/<int:master_id>', methods=['POST'])
@login_required
@seller_required
def delete_master(master_id):
    master = Masters.query.get(master_id)
    if not master:
        flash(f'Ошибка: Мастер с ID {master_id} не найден.', 'error')
        return redirect(url_for('seller.masters'))
    try:
        products_by_master = Product.query.filter_by(id_master=master.ID_master).all()
        if products_by_master:
            flash(f'Невозможно удалить мастера "{master.Name_master}", так как существуют связанные товары. Сначала переназначьте или удалите эти товары.', 'error')
            return redirect(url_for('seller.masters'))

        db.session.delete(master)
        db.session.commit()
        flash(f'Мастер "{master.Name_master}" успешно удален.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении мастера "{master.Name_master}": {str(e)}', 'error')

    return redirect(url_for('seller.masters'))
