from flask import Flask
from flask_bcrypt import Bcrypt
from ecommerceApp.models import db, login_manager


app = Flask(__name__)

app.secret_key = '156e497c1a5c51bbdfda262e57a1092c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/ecommerce_web_app'
app.url_map.strict_slashes = False
PAYPAL_CLIENT_ID = ''
PAYPAL_CLIENT_SECRET = ''
db.init_app(app)
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


app.register_blueprint(users)
app.register_blueprint(home)
app.register_blueprint(shop)
app.register_blueprint(about)
app.register_blueprint(product)
app.register_blueprint(contact)
app.register_blueprint(sustainability)
app.register_blueprint(cart)
app.register_blueprint(payment)
