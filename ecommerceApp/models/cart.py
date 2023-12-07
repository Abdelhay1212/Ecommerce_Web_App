from ecommerceApp.models import db


class Cart(db.Model):
    cart_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
