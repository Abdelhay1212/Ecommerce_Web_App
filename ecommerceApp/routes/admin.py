from ecommerceApp import db
from flask_login import current_user
from ecommerceApp.models.product import Product
from ecommerceApp.models.cart import Cart
from ecommerceApp.models.order import Order
from ecommerceApp.routes.utils import save_image, delete_image
from flask import Blueprint, render_template, redirect, url_for, flash, request


admin = Blueprint('admin', __name__)

@admin.route('/admin')
def control_panel():
    # checking if the user is authenticated
    if current_user.is_authenticated:
        # checking if the user is admin and render the control panel page
        # otherwise we return the home page
        if current_user.admin:
            # retrieving products from database and render it in control panel page
            products = Product.query.all()
            return render_template("control_panel.html", title="Control Panel", products=products)

    flash("You don't have the permissions to access that page!", category="info")
    return redirect(url_for('home.home_route'))


@admin.route('/admin/create-new-product', methods=['GET', 'POST'])
def create_new_product():
    # checking if the user is authenticated
    if current_user.is_authenticated:
        # checking if the user is admin and store the new product in the database
        # otherwise we return the home page
        if current_user.admin:
            # Receiving the product information from the form
            title = request.form['title']
            content = request.form['content']
            price = request.form['price']
            stock = request.form['stock']
            selled = request.form['selled']
            image_file = request.files['image']

            # saving the image in the path
            if image_file:
                image_name = save_image(image_file, 'static/images/products_images')

            # checking if the fields are filled
            # if not we flash a message and return the same page
            if title and content and price and stock and selled and image_name:
                # creating new product in the database
                product = Product(title=title,
                                    content=content,
                                    old_price=float(price) + 1,
                                    price=float(price),
                                    selled=int(selled),
                                    stock=int(stock),
                                    image=image_name
                                )

                db.session.add(product)
                db.session.commit()
            else:
                flash("All fields are required.", category="error")

            return redirect(url_for('admin.control_panel'))

    # if the user is not authenticated or doesn't have permissions to access this page
    flash("You don't have the permissions to access that page!", category="info")
    return redirect(url_for('home.home_route'))


@admin.route('/admin/edit-product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    # checking if the user is authenticated
    if current_user.is_authenticated:
        # checking if the user is admin
        # otherwise we return the home page
        if current_user.admin:
            # if request method is get we render the update prodact page
            if request.method == 'GET':
                product = Product.query.get(id)
                return render_template("update_product.html", title="Update Product", product=product)

            # Receiving the product information from the form
            title = request.form['title']
            content = request.form['content']
            price = request.form['price']
            stock = request.form['stock']
            selled = request.form['selled']
            image_file = request.files['image']

            # retreiving the product by its id
            product = Product.query.get(id)

            #checking if the product exist
            if product:
                # saving the image in the path if it's not the same image
                if image_file and product.image != image_file.filename:
                    image_name = save_image(image_file, 'static/images/products_images')
                    # delete the old image 
                    delete_image(product.image, 'static/images/products_images')
                    # save the new image
                    product.image = image_name

                # update the product information
                if title and content and price and stock and selled:
                    product.title = title
                    product.content = content
                    product.price = price
                    product.stock = stock
                    product.selled = selled

                # commit changes
                db.session.commit()

            return redirect(url_for('admin.control_panel'))
        
    # if the user is not authenticated or doesn't have permissions to access this page
    flash("You don't have the permissions to access that page!", category="info")
    return redirect(url_for('home.home_route'))




@admin.route('/admin/delete-product/<int:id>')
def delete_product(id):
    # checking if the user is authenticated
    if current_user.is_authenticated:
        # checking if the user is admin
        # otherwise we return the home page
        if current_user.admin:
            # retreiving the product by its id
            product = Product.query.get(id)
            cart = Cart.query.filter_by(product_id=id).first()
            order = Order.query.filter_by(product_id=id).first()

            # checking if the product exist
            if product:
                # delete the product from cart and order tables
                if cart:
                    db.session.delete(cart)
                if order:
                    db.session.delete(order)
                # delete the image of the product from the path
                delete_image(product.image, 'static/images/products_images')
                # delete the product from database
                db.session.delete(product)
                db.session.commit()

            return redirect(url_for('admin.control_panel'))

    # if the user is not authenticated or doesn't have permissions to access this page
    flash("You don't have the permissions to access that page!", category="info")
    return redirect(url_for('home.home_route'))
