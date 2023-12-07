from ecommerceApp.models import db


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    old_price = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    selled = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(20), nullable=False)

    orders = db.relationship('Order', backref='product', lazy=True)
    cart = db.relationship('Cart', backref='product', lazy=True)
