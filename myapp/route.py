from sqlalchemy import Engine
from myapp import app
from myapp import db
from myapp.models import Product, User, Category, Order, OrderDetail, Payment, Shipment, Review
from myapp.MyData import (CategoryJSON, ProductJSON, UserJSON, OrderJSON, 
                           OrderDetailJSON, PaymentJSON, ShipmentJSON, ReviewJSON)
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

# Home Route
@app.route('/')
def home_page():
    return 'Welcome to my web service'

# User Management

@app.route('/user', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([UserJSON(user).__dict__ for user in users])
    
    if request.method == 'POST':
        request_data = request.get_json()
        new_user = User(
            name=request_data['name'],
            email=request_data['email'],
            password=request_data['password']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(UserJSON(new_user).__dict__), 201

@app.route('/user/id/<uid>', methods=['GET', 'PUT', 'DELETE'])
def user_by_id(uid):
    user = User.query.filter_by(id=uid).first()
    if not user:
        return jsonify({'error': f'User not found with ID = {uid}'}), 404

    if request.method == 'GET':
        return jsonify(UserJSON(user).__dict__)
    
    if request.method == 'PUT':
        request_data = request.get_json()
        user.name = request_data['name']
        user.email = request_data['email']
        user.password = request_data['password']
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})

    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': f'User ID = {uid} has been deleted'})

# Product Management

@app.route('/product', methods=['GET', 'POST'])
def manage_products():
    if request.method == 'GET':
        products = Product.query.all()
        return jsonify([ProductJSON(product).__dict__ for product in products])
    
    if request.method == 'POST':
        request_data = request.get_json()
        new_product = Product(
            name=request_data['name'],
            category_id=request_data['category_id'],
            barcode=request_data['barcode'],
            price=request_data['price'],
            stock=request_data['stock']
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify(ProductJSON(new_product).__dict__), 201

@app.route('/product/id/<pid>', methods=['GET', 'PUT', 'DELETE'])
def product_by_id(pid):
    product = Product.query.filter_by(id=pid).first()
    if not product:
        return jsonify({'error': f'Product not found with ID = {pid}'}), 404

    if request.method == 'GET':
        return jsonify(ProductJSON(product).__dict__)
    
    if request.method == 'PUT':
        request_data = request.get_json()
        product.name = request_data['name']
        product.category_id = request_data['category_id']
        product.barcode = request_data['barcode']
        product.price = request_data['price']
        product.stock = request_data['stock']
        db.session.commit()
        return jsonify({'message': 'Product updated successfully'})

    if request.method == 'DELETE':
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': f'Product ID = {pid} has been deleted'})

# Order Management

@app.route('/order', methods=['GET', 'POST'])
def manage_orders():
    if request.method == 'GET':
        orders = Order.query.all()
        return jsonify([OrderJSON(order).__dict__ for order in orders])
    
    if request.method == 'POST':
        request_data = request.get_json()
        new_order = Order(user_id=request_data['user_id'])
        db.session.add(new_order)
        db.session.commit()

        for item in request_data['products']:
            product = Product.query.filter_by(id=item['product_id']).first()
            if product:
                order_detail = OrderDetail(order_id=new_order.id, product_id=product.id, quantity=item['quantity'], price=product.price)
                db.session.add(order_detail)
            else:
                return jsonify({'error': f'Product not found with ID = {item["product_id"]}'}), 404

        db.session.commit()
        return jsonify(OrderJSON(new_order).__dict__), 201

@app.route('/order/id/<oid>', methods=['GET', 'PUT', 'DELETE'])
def order_by_id(oid):
    order = Order.query.filter_by(id=oid).first()
    if not order:
        return jsonify({'error': f'Order not found with ID = {oid}'}), 404

    if request.method == 'GET':
        return jsonify(OrderJSON(order).__dict__)
    
    if request.method == 'PUT':
        request_data = request.get_json()
        order.status = request_data.get('status', order.status)
        db.session.commit()
        return jsonify({'message': 'Order updated successfully'})

    if request.method == 'DELETE':
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': f'Order ID = {oid} has been deleted'})
    
# Payment Management

@app.route('/payment', methods=['POST'])
def add_payment():
    request_data = request.get_json()
    order_id = request_data['order_id']
    payment = Payment(
        order_id=order_id,
        amount=request_data['amount'],
        payment_method=request_data['payment_method'],
        status=request_data['status']
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify(PaymentJSON(payment).__dict__), 201

# Shipment Management

@app.route('/shipment', methods=['POST'])
def add_shipment():
    request_data = request.get_json()
    shipment = Shipment(
        order_id=request_data['order_id'],
        address_id=request_data['address_id'],
        shipment_date=request_data.get('shipment_date'),
        delivery_date=request_data.get('delivery_date'),
        tracking_number=request_data.get('tracking_number'),
        status=request_data.get('status')
    )
    db.session.add(shipment)
    db.session.commit()
    return jsonify(ShipmentJSON(shipment).__dict__), 201

# Review Management

@app.route('/review', methods=['POST'])
def add_review():
    request_data = request.get_json()
    review = Review(
        product_id=request_data['product_id'],
        user_id=request_data['user_id'],
        rating=request_data['rating'],
        comment=request_data.get('comment')
    )
    db.session.add(review)
    db.session.commit()
    return jsonify(ReviewJSON(review).__dict__), 201

# Error Handling (unchanged)

@app.errorhandler(KeyError)
def key_error(err):
    app.logger.exception(err)
    return jsonify({'message': f'Invalid key {err}'}), 400

@app.errorhandler(SQLAlchemyError)
def sql_error(err):
    app.logger.exception(err)
    message = str(err.__dict__['orig'])
    return jsonify({'message': f'{message}'}), 400

@app.errorhandler(Exception)
def exception_error(err):
    app.logger.exception(err)
    return jsonify({'message': f'{err}'}), 500