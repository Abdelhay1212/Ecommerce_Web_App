from flask import Blueprint, render_template
from ecommerceApp.models.product import Product


shop = Blueprint('shop', __name__)

@shop.route('/shop')
def shop_route():
    products = Product.query.all()

    if products is None:
        products = []

    return render_template("shop.html", products=products, title="Shop")
