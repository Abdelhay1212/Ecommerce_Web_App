from ecommerceApp.models import db
from ecommerceApp.models.cart import Cart
from ecommerceApp.models.user import User
from ecommerceApp.models.product import Product
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, redirect, url_for, flash


cart = Blueprint('cart', __name__)

@cart.route('/cart')
def cart_route():
    items = None

    if current_user.is_authenticated:
        items = Cart.query.filter_by(user=current_user).all()

    products = []
    total = 0

    if items:
        for item in items:
            product = Product.query.filter_by(product_id=item.product_id).first()

            total += (product.price * item.amount)

            product.amount = item.amount
            product.price = round(product.price * item.amount, 2)
            products.append(product)

    total = round(total, 2)

    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))

    return render_template("cart.html", title="Cart", products=products, total=total)


@cart.route('/add_to_cart/<int:product_id>/<int:user_id>', methods=['GET', 'POST'])
def add_to_cart(product_id, user_id):
    if current_user.is_authenticated:
        if request.method == 'POST':
            user = User.query.get(user_id)
            product = Product.query.get(product_id)

            if user and product:
                cart_entry = Cart.query.filter_by(user=user, product=product).first()

                if cart_entry:
                    flash('This item is already added to your cart!', category='info')
                else:
                    quantity = int(request.form.get('amount'))
                    if quantity <= product.stock:
                        new_cart_entry = Cart(user=user, product=product, amount=quantity)
                        db.session.add(new_cart_entry)
                        flash('One Item Has Been Added To Your Cart!', 'success')

                db.session.commit()
    else:
        flash('You should log in to use this funcionality!', 'warning')

    return redirect(url_for('product.product_route', product_id=product_id))


@cart.route('/update_to_cart')
def update_to_cart():
    if current_user.is_authenticated:
        user_id = request.args.get('user_id')
        product_id = request.args.get('product_id')

        user = User.query.get(user_id)
        product = Product.query.get(product_id)

        if user and product:
            cart_entry = Cart.query.filter_by(user=user, product=product).first()

            if cart_entry:
                if request.args.get('opt') == 'minus':
                    cart_entry.amount -= 1
                    if cart_entry.amount <= 0:
                        db.session.delete(cart_entry)

                elif request.args.get('opt') == 'plus':
                    if cart_entry.amount < product.stock:
                        cart_entry.amount += 1

                db.session.commit()
                flash('Your cart has been updated successfully!', category='success')
    else:
        flash('You should log in to use this funcionality!', category='warning')

    return redirect(url_for('cart.cart_route'))


@cart.route('/delete_in_cart')
def delete_in_cart():
    if current_user.is_authenticated:
        user_id = request.args.get('user_id')
        product_id = request.args.get('product_id')

        user = User.query.get(user_id)
        product = Product.query.get(product_id)

        if user and product:
            cart_entry = Cart.query.filter_by(user=user, product=product).first()
            db.session.delete(cart_entry)
            db.session.commit()
            flash('You succefully deleted one item!', category='success')
    else:
        flash('You should log in to use this funcionality!', category='warning')

    return redirect(url_for('cart.cart_route'))


@cart.app_context_processor
def inject_num_of_items_in_cart():
    items = None

    if current_user.is_authenticated:
        items = Cart.query.filter_by(user=current_user).all()

    num_of_items = 0

    if items:
        num_of_items = len(items)

    return dict(num_of_items=num_of_items)
