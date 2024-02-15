# Define all the models used by the application
from Ecommerce import db, login_manager
from flask_login import UserMixin
from .tools import hash_pass

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(500), unique=False, nullable=False)
    country = db.Column(db.String(120), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    address = db.Column(db.String(120), unique=False, nullable=False)
    phone = db.Column(db.String(120), unique=False, nullable=False)

    cart_item = db.relationship("Cart", backref="user", cascade="all, delete, delete-orphan")
    order_item = db.relationship("Order", backref="user", cascade="all, delete, delete-orphan")


    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)
    desc = db.Column(db.Text, nullable=False)
    image_1 = db.Column(db.String(256), nullable=False, default='image1.jpg')

    cart_item = db.relationship("Cart", backref="product", cascade="all, delete, delete-orphan")
    order_item = db.relationship("Order", backref="product", cascade="all, delete, delete-orphan")


class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

