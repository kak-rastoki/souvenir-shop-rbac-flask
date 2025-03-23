"""
Модуль Панели администратора
--------------------------------------------------
Описание:

"""


from flask_login import login_required
from datetime import datetime
import base64
from flask import render_template,url_for, redirect, request, jsonify, get_flashed_messages,flash
from decorators import admin_required
from app import db, Users, Masters, Categories, Product, Genders
from . import admin_bp


@admin_bp.route('/aPbAs3')
@login_required
@admin_required
def APbaseShow():
    return render_template('adminBase.html')

@admin_bp.route('/admin')
@login_required
@admin_required
def Admin_products():
    masters = Masters.query.all()
    categories = Categories.query.all()
    products = Product.query.all()


    products_data = []
    for product in products:

        category = Categories.query.get(product.id_category)
        master = Masters.query.get(product.id_master)


        products_data.append({
            'ID_product': product.ID_product,
            'Name_product': product.Name_product,
            'Cost_product': product.Cost_product,
            'Description_product': product.Description_product,
            'Category_name': category.Name_category if category else 'Неизвестно',
            'Master_name': master.Name_master if master else 'Неизвестно',
            'IsNew_product': product.IsNew_product
        })



    errors1 = get_flashed_messages(category_filter=['error1'])
    if not errors1:
        errors1 = {}
    errors2=get_flashed_messages(category_filter=['error2'])
    if not errors2:
        errors2 = {}


    return render_template('admin/A_products.html', masters=masters, categories=categories, products=products_data, errors2=errors2,errors1=errors1)

@admin_bp.route('/admin/add-product', methods=['GET', 'POST'])
@login_required
@admin_required
def AP_add_product():

    errors2=get_flashed_messages(category_filter=['error'])
    if not errors2:
        errors2 = {}

    masters = Masters.query.all()
    categories = Categories.query.all()
    #  Получаем все товары
    products = Product.query.all()
    products_data = []
    for product in products:
        #  связанные категории и мастера для каждого товара
        category = Categories.query.get(product.id_category)
        master = Masters.query.get(product.id_master)


        products_data.append({
            'ID_product': product.ID_product,
            'Name_product': product.Name_product,
            'Cost_product': product.Cost_product,
            'Description_product': product.Description_product,
            'Category_name': category.Name_category if category else 'Неизвестно',  # Заменяем ID на имя
            'Master_name': master.Name_master if master else 'Неизвестно',
            'IsNew_product': product.IsNew_product
        })

    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        new_product = request.form.get('newProduct') == 'on'
        master = request.form.get('master')
        category = request.form.get('category')
        file = request.files['file']

        if not name or not price:
            flash("Все поля, кроме 'Новинка', обязательны для заполнения!", "error")
            return redirect(url_for('admin.AP_add_product'))

        if category == "Выберите категорию" or master == "Выберите мастера":
            flash("Пожалуйста, выберите категорию и мастера!", "error")
            return redirect(url_for('admin.AP_add_product'))

        try:
            price = float(price)  # Проверяем, что цена - число
        except ValueError:
            flash("Цена должна быть числом!", "error")
            return redirect(url_for('admin.AP_add_product'))

        # Сохранение в базу данных
        new_product_entry = Product(
            Name_product=name,
            Cost_product=price,
            IsNew_product=new_product,
            id_master=master,
            id_category=category,
            image_product = file.read()
        )
        db.session.add(new_product_entry)
        db.session.commit()

        flash("Товар успешно добавлен!", "success")
        return redirect(url_for('admin.Admin_products'))

    return render_template('admin/A_products.html', masters=masters, categories=categories,products=products_data,errors2=errors2)

@admin_bp.route('/admin/products_table',methods=['GET'])
@login_required
@admin_required
def display_products():
     # Получаем все товары
    products = Product.query.all()

    # Подготавливаем данные о товарах для передачи в шаблон
    products_data = []
    for product in products:
        # Получаем связанные категорию и мастера для каждого товара
        category = Categories.query.get(product.id_category)
        master = Masters.query.get(product.id_master)

        # Создаем словарь с данными
        products_data.append({
            'ID_product': product.ID_product,
            'Name_product': product.Name_product,
            'Cost_product': product.Cost_product,
            'Description_product': product.Description_product,
            'Category_name': category.Name_category if category else 'Неизвестно', # Заменяем ID на имя
            'Master_name': master.Name_master if master else 'Неизвестно', # Заменяем ID на имя
            'IsNew_product': product.IsNew_product
        })

    return render_template('admin/A_products.html',products=products_data)


@admin_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_product(id):
    product= Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        print (f'Продукт {product.ID_product} - {product.Name_product} успешно удален')
    else:
        print (f'Внутренняя ошибка сервера. Продукт {product.ID_product} {product.Name_product} - не найден')

    return redirect(url_for('admin.Admin_products'))



@admin_bp.route('/api/product/<int:product_id>', methods=['GET'])
@login_required
@admin_required
def get_product_api(product_id):
    product = Product.query.get_or_404(product_id)


    product_data = {
        'ID_product': product.ID_product,
        'Name_product': product.Name_product,
        'Cost_product': product.Cost_product,
        'IsNew_product': product.IsNew_product,
        'id_master': product.id_master,
        'id_category': product.id_category,
        'Description_product': product.Description_product

    }

    return jsonify(product_data)



# Route to change Product
@admin_bp.route('/admin/edit_product', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product():
    error_messages = ()

    if request.method == 'POST':
        edit_code = request.form.get('editCode')
        edit_name = request.form.get('editName')
        edit_price = request.form.get('editPrice')
        edit_new_product = request.form.get('editNewProduct') == 'on'
        edit_master = request.form.get('editMaster')
        edit_category = request.form.get('editCategory')
        edit_description = request.form.get('editDescription')
        edit_file = request.files['editFile']

        product = Product.query.get(edit_code)

        print (str(edit_name))
        # Валидация
        if not edit_name or not edit_price:
            error_messages="Заполните все поля!"

        if edit_category == "Выберите категорию" or edit_master == "Выберите мастера из списка":
            error_messages= "Пожалуйста, выберите категорию и мастера!"

        # try:
        #     edit_price = float(edit_price)  # Проверяем, что цена - число
        # except ValueError:
        #     error_messages["priceisint"] = "Цена должна быть числом!"
        #     return redirect(url_for('AP_add_product')) # Передаем ошибки


        if product:
            #Сохраняем данные
            product.Name_product = edit_name
            product.Cost_product = edit_price
            product.IsNew_product = edit_new_product
            product.id_master = edit_master
            product.id_category = edit_category
            product.Description_product = edit_description
            product.image_product = edit_file.read()
        else:
            print (f'Внутренняя ошибка сервера. Продукт {product.ID_product} {product.Name_product} - не найден')
            error_messages = "Продукт не найден"


        if  error_messages:
           flash(error_messages, 'error2')
           return redirect(url_for('admin.Admin_products'))
        else:
            db.session.commit()
            flash("Изменения выполнены успешно!", "error2")
            print(f'Продукт {product.ID_product} - {product.Name_product} успешно изменен')
            return redirect(url_for('admin.Admin_products')) # успешный редирект
    return redirect(url_for('admin.Admin_products'))


#---------AP - Users ---------
@admin_bp.route('/admin/users')
@login_required
@admin_required
def Admin_users():
    users = Users.query.all()
    errors2=get_flashed_messages(category_filter=['error2'])
    if not errors2:
        errors2 = {}
    return render_template('admin/A_users.html', users=users, errors2=errors2)

@admin_bp.route('/admin/edit_user', methods=['POST','GET'])
@login_required
@admin_required
def edit_user():
    error_messages = ""
    if request.method == 'POST':
        edit_code = request.form.get('editCode')
        edit_name = request.form.get('editName')
        edit_phone = request.form.get('editPhone')
        edit_email = request.form.get('editEmail')
        edit_bday = request.form.get('editBday')
        edit_avatar = request.files['editAvatar']

        user = Users.query.get(edit_code)

        if not edit_name or not edit_phone or not edit_email:
            error_messages = "Заполните все поля!"

        if user:
           user.Name_user = edit_name
           user.phone_number = edit_phone
           user.mail_user = edit_email
           user.avatar = edit_avatar.read()

           if edit_bday:
               user.BirthDay_user = datetime.strptime(edit_bday,'%Y-%m-%d').date()
           else:
               user.BirthDay_user = None
        else:
            print(f'Внутренняя ошибка сервера. Пользователь {user.ID_user} - не найден')
            error_messages = "Пользователь не найден"

        if error_messages:
            flash(error_messages, 'error2')
            return redirect(url_for('admin.Admin_users'))
        else:
            db.session.commit()
            flash("Изменения выполнены успешно", 'error2')
            print(f'Пользователь {user.ID_user} - {user.Name_user} успешно изменен')
            return redirect(url_for('admin.Admin_users'))


@admin_bp.route('/api/user/<int:user_id>', methods=['GET'])
@login_required
@admin_required
def get_user_api(user_id):
    user = Users.query.get_or_404(user_id)
    avatar_base64 = None
    if user.avatar:
        avatar_base64 = base64.b64encode(user.avatar).decode('utf-8')
    user_data = {
        'ID_user': user.ID_user,
        'Name_user': user.Name_user,
        'phone_number': user.phone_number,
        'mail_user': user.mail_user,
        'BirthDay_user': user.BirthDay_user.isoformat() if user.BirthDay_user else None,
        'created_at': user.created_at.isoformat(),
        'avatar': avatar_base64

    }

    return jsonify(user_data)

@admin_bp.route('/delete_user/<int:id>', methods=['POST','GET']) #перепроверить запросы
@login_required
@admin_required
def delete_user(id):
    user= Users.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        print (f'Пользователь {user.ID_user} - {user.Name_user} успешно удален')
    else:
        print (f'Внутренняя ошибка сервера. Пользователь {user.ID_user} - не найден')

    return redirect(url_for('admin.Admin_users'))

#---------AP - Category ---------
# Route to add category
@admin_bp.route('/admin/add_category', methods=['POST'])
@login_required
@admin_required
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        if not name:
            flash("Наименование категории обязательно для заполнения!", 'error1')
            return redirect(url_for('admin.Admin_categories'))

        new_category = Categories(
            Name_category=name,
            Discription_category=description
        )
        db.session.add(new_category)
        db.session.commit()

        flash("Категория успешно добавлена!", 'success')
        return redirect(url_for('admin.Admin_categories'))
    return render_template('admin/categories_admin.html')



# Route to delete category
@admin_bp.route('/delete_category/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_category(id):
    category = Categories.query.get(id)
    if category:
        db.session.delete(category)
        db.session.commit()
        print(f'Категория {category.ID_categories} - {category.Name_category} успешно удалена')
    else:
        print(f'Внутренняя ошибка сервера. Категория не найдена')

    return redirect(url_for('admin.Admin_categories'))


# Route to api get category
@admin_bp.route('/api/category/<int:category_id>', methods=['GET'])
@login_required
@admin_required
def get_category_api(category_id):
    category = Categories.query.get_or_404(category_id)

    category_data = {
        'ID_categories': category.ID_categories,
        'Name_category': category.Name_category,
        'Discription_category': category.Discription_category
    }

    return jsonify(category_data)

# Route to edit category
@admin_bp.route('/admin/edit_category', methods=['GET','POST'])
@login_required
@admin_required
def edit_category():
    error_messages = ()

    if request.method == 'POST':
         edit_code = request.form.get('editCode')
         edit_name = request.form.get('editName')
         edit_description = request.form.get('editDescription')
         category = Categories.query.get(edit_code)

         if not edit_name:
             error_messages = "Заполните все обязательные поля"


         if category:
            category.Name_category = edit_name
            category.Discription_category = edit_description
         else:
            print(f'Внутренняя ошибка сервера. Категория {category.ID_categories} - не найдена')
            error_messages = "Категория не найдена"


         if error_messages:
            flash(error_messages, 'error2')
            return redirect(url_for('admin.Admin_categories'))
         else:
            db.session.commit()
            flash("Изменения выполнены успешно!", 'error2')
            print(f'Категория {category.ID_categories} - {category.Name_category} успешно изменена')
            return redirect(url_for('admin.Admin_categories'))

# new route for categories page
@admin_bp.route('/admin/categories')
@login_required
@admin_required
def Admin_categories():
    categories = Categories.query.all()
    errors1=get_flashed_messages(category_filter=['error1'])
    if not errors1:
        errors1 = {}
    errors2=get_flashed_messages(category_filter=['error2'])
    if not errors2:
        errors2 = {}
    return render_template('admin/categories_admin.html', categories=categories, errors1=errors1, errors2=errors2)

# Route to display masters
@admin_bp.route('/admin/masters')
@login_required
@admin_required
def Admin_masters():
    masters = Masters.query.all()
    genders=Genders.query.all()
    # данные о мастерах для передачи в шаблон
    masters_data = []
    for master in masters:
        #  связанный пол для каждого мастера
        gender = Genders.query.get(master.id_gender)

        #  словарь с данными
        masters_data.append({
            'ID_master': master.ID_master,
            'Name_master': master.Name_master,
            'gender_name': gender.gender_name if gender else "Неизвестно" ,
              'id_gender': master.id_gender,

        })


    errors1=get_flashed_messages(category_filter=['error1'])
    if not errors1:
        errors1 = {}
    errors2=get_flashed_messages(category_filter=['error2'])
    if not errors2:
        errors2 = {}
    return render_template('admin/masters_admin.html', masters=masters_data, genders=genders, errors1=errors1, errors2=errors2)

# Route to add master
@admin_bp.route('/admin/add_master', methods=['GET','POST'])
@login_required
@admin_required
def add_master():
     if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')

        if not name:
            flash("Наименование мастера обязательно для заполнения!", 'error1')
            return redirect(url_for('admin.Admin_masters'))

        if gender == "Выберите пол":
             flash("Выберите пол", 'error1')
             return redirect(url_for('admin.Admin_masters'))

        new_master = Masters(
            Name_master=name,
            id_gender=gender,
        )
        db.session.add(new_master)
        db.session.commit()

        flash("Мастер успешно добавлен!", 'success')
        return redirect(url_for('admin.Admin_masters'))
     return redirect(url_for('admin.Admin_masters'))

# Route to delete master
@admin_bp.route('/delete_master/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_master(id):
    master = Masters.query.get(id)
    if master:
        db.session.delete(master)
        db.session.commit()
        print(f'Мастер {master.ID_master} - {master.Name_master} успешно удален')
    else:
        print(f'Внутренняя ошибка сервера. Мастер не найден')

    return redirect(url_for('admin.Admin_masters'))


# Route to api get master
@admin_bp.route('/api/master/<int:master_id>', methods=['GET'])
@login_required
@admin_required
def get_master_api(master_id):
    master = Masters.query.get_or_404(master_id)

    master_data = {
        'ID_master': master.ID_master,
        'Name_master': master.Name_master,
        'id_gender': master.id_gender,


    }

    return jsonify(master_data)

# Route to edit master
@admin_bp.route('/admin/edit_master', methods=['POST'])
@login_required
@admin_required
def edit_master():
    error_messages = ()

    if request.method == 'POST':
         edit_code = request.form.get('editCode')
         edit_name = request.form.get('editName')
         edit_gender = request.form.get('editGender')

         master = Masters.query.get(edit_code)

         if not edit_name:
             error_messages = "Заполните все обязательные поля"
         if edit_gender == "Выберите пол":
            error_messages = "Выберите пол"
         if master:
            master.Name_master = edit_name
            master.id_gender = edit_gender
         else:
            print(f'Внутренняя ошибка сервера. Мастер {master.ID_master} - не найден')
            error_messages = "Мастер не найден"


         if error_messages:
            flash(error_messages, 'error2')
            return redirect(url_for('admin.Admin_masters'))
         else:
            db.session.commit()
            flash("Изменения выполнены успешно!", 'error2')
            print(f'Мастер {master.ID_master} - {master.Name_master} успешно изменен')
            return redirect(url_for('admin.Admin_masters'))
    return redirect(url_for('admin.Admin_masters'))
