from ecommerceApp.models.product import Product
from flask import Blueprint, render_template, request, redirect, url_for, flash


product = Blueprint('product', __name__)

@product.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_route(product_id):
    data = Product.query.get(product_id)

    if data is None:
        data = {}

    if request.method == 'POST':
        flash('You Have To Login To Add Items Into Your Cart!', 'info')
        return redirect(url_for('users.login'))

    return render_template("product.html", data=data)

