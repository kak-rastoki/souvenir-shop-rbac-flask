from flask import render_template
from . import catalog_bp

@catalog_bp.route('/catalog')
def catalog():
    return render_template('catalog.html', title='Каталог')

@catalog_bp.route('/<path:path>')
def catalog_path(path):
    return render_template('catalog.html', title='Каталог')

@catalog_bp.route('/catalog/cart')
def cart_react():
    return render_template('catalog.html')
