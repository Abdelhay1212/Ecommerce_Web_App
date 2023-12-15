import os
from flask import Flask
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from ecommerceApp.models import db, login_manager


app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@localhost:3306/{db_name}'

# mail configurations
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'noreply@gmail.com'

app.url_map.strict_slashes = False
PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET')

db.init_app(app)
mail = Mail(app)
bcrypt = Bcrypt(app)
login_manager.init_app(app, add_context_processor=True)

login_manager.login_view = 'users.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = "info"
login_manager.session_protection = "strong"


from ecommerceApp.routes.user import users
from ecommerceApp.routes.home import home
from ecommerceApp.routes.shop import shop
from ecommerceApp.routes.about import about
from ecommerceApp.routes.product import product
from ecommerceApp.routes.contact import contact
from ecommerceApp.routes.sustainability import sustainability
from ecommerceApp.routes.cart import cart
from ecommerceApp.routes.payment import payment
from ecommerceApp.routes.admin import admin


app.register_blueprint(users)
app.register_blueprint(home)
app.register_blueprint(shop)
app.register_blueprint(about)
app.register_blueprint(product)
app.register_blueprint(contact)
app.register_blueprint(sustainability)
app.register_blueprint(cart)
app.register_blueprint(payment)
app.register_blueprint(admin)
