from . import seller_bp
from flask_login import login_required, current_user
from datetime import datetime
import base64
from flask import render_template,url_for, redirect, request, jsonify, get_flashed_messages,flash,current_app
from decorators import admin_required,seller_required
from models import db, Users, Masters, Categories, Product, Genders, Order, OrderProduct, Review, OrderStatus
from sqlalchemy import func
import base64
from PIL import Image
import io

THUMBNAIL_SIZE = 50

@seller_bp.route('/seller')
@login_required
@seller_required
def show_orders():
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


    return render_template('/dashboard.html',
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

    # Используем категории flash-сообщений 'error' и 'success'
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
