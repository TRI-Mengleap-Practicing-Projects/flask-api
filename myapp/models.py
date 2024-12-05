from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from myapp import db
from datetime import datetime

class User(db.Model):
     __tablename__ = 'user'
     
     id = Column(Integer, primary_key=True, autoincrement=True)
     name = Column(String(50), nullable=False, unique=True)
     email = Column(String(100), unique=True, nullable=False)
     password = Column(String(128), nullable=False)
     created_at = Column(DateTime, default=datetime.utcnow)

     addresses = db.relationship('Address', back_populates='user', lazy='dynamic')
     orders = db.relationship('Order', back_populates='user', lazy='dynamic')
     reviews = db.relationship('Review', back_populates='user', lazy='dynamic')

class Address(db.Model):
     __tablename__ = 'address'
     
     id = Column(Integer, primary_key=True, autoincrement=True)
     user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
     address_line1 = Column(String(100), nullable=False)
     address_line2 = Column(String(100), nullable=True)
     city = Column(String(50), nullable=False)
     state = Column(String(50), nullable=False)
     zip_code = Column(String(20), nullable=False)
     country = Column(String(50), nullable=False)

     user = db.relationship('User', back_populates='addresses')

class Category(db.Model):
     __tablename__ = 'category'
     
     id = Column(Integer, primary_key=True, autoincrement=True)
     name = Column(String(50), nullable=False)

     products = db.relationship('Product', back_populates='category', lazy='dynamic')

class Product(db.Model):
     __tablename__ = 'product'
     
     id = Column(Integer, primary_key=True, autoincrement=True)
     name = Column(String(100), nullable=False)
     category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
     barcode = Column(String(100), unique=True, nullable=False)
     price = Column(Float, nullable=False)
     stock = Column(Integer, nullable=False)
     created_at = Column(DateTime, default=datetime.utcnow)

     category = db.relationship('Category', back_populates='products')
     reviews = db.relationship('Review', back_populates='product', lazy='dynamic')
     order_details = db.relationship('OrderDetail', back_populates='product', lazy='dynamic')

class Order(db.Model):
     __tablename__ = 'order'
     
     id = Column(Integer, primary_key=True, autoincrement=True)
     user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
     order_date = Column(DateTime, default=datetime.utcnow)
     status = Column(String(50))
     total_amount = Column(Float)

     user = db.relationship('User', back_populates='orders')
     order_details = db.relationship('OrderDetail', back_populates='order', lazy='dynamic')
     payment = db.relationship('Payment', back_populates='order', uselist=False)
     shipment = db.relationship('Shipment', back_populates='order', uselist=False)

class OrderDetail(db.Model):
     __tablename__ = 'order_detail'
     
     id = Column(Integer, primary_key=True, autoincrement=True)
     order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
     product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
     quantity = Column(Integer, nullable=False)
     price = Column(Float, nullable=False)

     order = db.relationship('Order', back_populates='order_details')
     product = db.relationship('Product', back_populates='order_details')

class Payment(db.Model):
     __tablename__ = 'payment'
     
     id = Column(Integer, primary_key=True, autoincrement=True)
     order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
     amount = Column(Float, nullable=False)
     payment_date = Column(DateTime, default=datetime.utcnow)
     payment_method = Column(String(50))
     status = Column(String(50))

     order = db.relationship('Order', back_populates='payment')

class Shipment(db.Model):
     __tablename__ = 'shipment'
     
     id = Column(Integer, primary_key=True, autoincrement=True)
     order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
     address_id = Column(Integer, ForeignKey('address.id'), nullable=False)
     shipment_date = Column(DateTime)
     delivery_date = Column(DateTime)
     tracking_number = Column(String(100))
     status = Column(String(50))

     order = db.relationship('Order', back_populates='shipment')
     address = db.relationship('Address')

class Review(db.Model):
     __tablename__ = 'review'
     
     id = Column(Integer, primary_key=True, autoincrement=True)
     product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
     user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
     rating = Column(Integer, nullable=False)
     comment = Column(Text)
     review_date = Column(DateTime, default=datetime.utcnow)
     product = db.relationship('Product', back_populates='reviews')
     user = db.relationship('User', back_populates='reviews')