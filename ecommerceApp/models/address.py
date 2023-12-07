from ecommerceApp.models import db


class Address(db.Model):
    address_id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    street = db.Column(db.String(50), nullable=False)
    home = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
