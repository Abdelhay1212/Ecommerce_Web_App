from ecommerceApp.models import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), default="default.jpg")

    orders = db.relationship('Order', backref='user', lazy=True)
    cart = db.relationship('Cart', backref='user', lazy=True)
    addresses = db.relationship('Address', backref='user', lazy=True)

    def get_id(self):
        return str(self.user_id)
