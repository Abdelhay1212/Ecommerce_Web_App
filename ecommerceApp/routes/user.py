from ecommerceApp import bcrypt, db
from ecommerceApp.models.user import User
from ecommerceApp.routes.utils import save_image, delete_image
from flask_login import login_user, current_user, logout_user
from ecommerceApp.routes.forms import LoginForm, RegistrationForm, UpdateAccountForm
from flask import Blueprint, render_template, redirect, url_for, flash, request


users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.home_route'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home.home_route'))
        else:
            flash(f'Login Unsuccessful, Please check email and password!', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.home_route'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template("register.html", title="Register", form=form)


@users.route('/account', methods=['GET', 'POST'])
def account():
    if current_user.is_authenticated:
        form = UpdateAccountForm()
        if form.validate_on_submit():
            if form.image_file.data:
                image_file = save_image(form.image_file.data, 'static/images/users_images')
                if image_file != 'default.jpg':
                    delete_image(current_user.image_file, 'static/images/users_images')
                current_user.image_file = image_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('users.account'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
        image_file = url_for('static', filename='images/users_images/' + current_user.image_file)
        return render_template('account.html', title='Account', image_file=image_file, form=form)
    else:
        flash('You have to log in to access you account!')
        return redirect(url_for('home.home_route'))


@users.route('/logout')
def logout():

    if current_user.is_authenticated:
        logout_user()
    
    return redirect(url_for('home.home_route'))
