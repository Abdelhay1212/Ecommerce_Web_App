from ecommerceApp.models import db
from ecommerceApp.models.product import Product
from ecommerceApp.models.newsletter import NewsLetter
from flask import Blueprint, render_template, request, redirect, url_for


home = Blueprint('home', __name__)

@home.route('/', methods=['GET', 'POST'])
@home.route('/home', methods=['GET', 'POST'])
def home_route():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            subscriber = NewsLetter.query.filter_by(email=email).first()
            if subscriber is None:
                subscriber = NewsLetter(email=email)
                db.session.add(subscriber)
                db.session.commit()

        return redirect(url_for('home.home_route'))

    top_products = Product.query.order_by(Product.selled.desc()).limit(4).all()

    if top_products is None:
        top_products = []

    return render_template("home.html", top_products=top_products, title="Home")
