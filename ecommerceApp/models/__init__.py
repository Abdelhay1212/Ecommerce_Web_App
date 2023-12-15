from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from ecommerceApp.models.user import User
from ecommerceApp.models.product import Product
from ecommerceApp.models.order import Order
from ecommerceApp.models.address import Address
from ecommerceApp.models.newsletter import NewsLetter
from ecommerceApp.models.cart import Cart
