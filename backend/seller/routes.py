from . import seller_bp
from flask_login import login_required
from datetime import datetime
import base64
from flask import render_template,url_for, redirect, request, jsonify, get_flashed_messages,flash
from decorators import admin_required,seller_required
from models import db, Users, Masters, Categories, Product, Genders, Order, OrderProduct, Review, OrderStatus
from sqlalchemy import func


@seller_bp.route('/seller')
@login_required
@seller_required
def show_orders():
  return render_template('seller/orders.html')


@seller_bp.route('/seller/bAsE')
@login_required
@seller_required
def show_base():
  return render_template('sellerbase.html')


@seller_bp.route('/seller/dashboard')
@login_required
@seller_required
def dashboard():
    total_products = Product.query.count()
    total_orders = Order.query.count()
    completed_orders_count = Order.query.filter_by(Status_order="завершен").count()
    pending_orders_count = Order.query.filter_by(Status_order="активен").count()
    cart_orders_count = Order.query.filter_by(Status_order="неактивен").count()


    latest_orders = Order.query.order_by(Order.Data_order.desc()).limit(5).all()


    return render_template('seller/dashboard.html',
                            total_products=total_products,
                            total_orders=total_orders,
                            completed_orders_count=completed_orders_count,
                            pending_orders_count=pending_orders_count,
                            cart_orders_count=cart_orders_count,
                            latest_orders=latest_orders,
                            current_user=current_user
                          )
