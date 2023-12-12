import json
import base64
import requests
from ecommerceApp import db
from flask_login import current_user
from ecommerceApp.models.cart import Cart
from ecommerceApp.models.order import Order
from ecommerceApp.models.product import Product
from ecommerceApp.models.address import Address
from flask import request, jsonify, Blueprint, render_template, flash
from ecommerceApp import PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET


payment = Blueprint('payment', __name__)

BASE_URL = "https://api-m.sandbox.paypal.com"

def generate_access_token():
    if not PAYPAL_CLIENT_ID or not PAYPAL_CLIENT_SECRET:
        raise Exception("MISSING_API_CREDENTIALS")

    credentials_string = f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}"
    auth_bytes = base64.b64encode(credentials_string.encode('utf-8'))
    auth = auth_bytes.decode('utf-8')

    url = f"{BASE_URL}/v1/oauth2/token"
    headers = {
        "Authorization": f"Basic {auth}",
    }

    data = {
        "grant_type": "client_credentials",
    }

    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

    data = response.json()
    return data['access_token']


def create_order(cart):
    access_token = generate_access_token()

    if current_user.is_authenticated:
        # retreiving the items in the cart
        items = Cart.query.filter_by(user_id=current_user.user_id).all()

        # init the total price
        total = 0

        # looping over the items to get the products price and quantity
        for item in items:
            product = Product.query.get(item.product_id)
            total += (product.price * item.amount)

        # saving the address of the customer
        address = Address.query.filter_by(user=current_user).first()

        # updating address if it's already exist, otherwise we create a new one
        if address:
            address.country = cart['country']
            address.city = cart['city']
            address.street = cart['street']
            address.home = int(cart['home'])
        else:
            address = Address(user=current_user,
                                country=cart['country'],
                                city=cart['city'],
                                street=cart['street'],
                                home=cart['home'])
            # adding new address to the database
            db.session.add(address)

        # commiting changes to the database
        db.session.commit()

    url = f'{BASE_URL}/v2/checkout/orders'
    payload = {
        'intent': "CAPTURE",
        'purchase_units': [
            {
                'amount': {
                    'currency_code': "USD",
                    'value': total
                },
            },
        ],
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    payload_json = json.dumps(payload)

    response = requests.post(url, data=payload_json, headers=headers)
    response.raise_for_status()

    jsonResponse = response.json()

    return jsonResponse


def capture_order(order_id):
    access_token = generate_access_token()
    url = f'{BASE_URL}/v2/checkout/orders/{order_id}/capture'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.post(url, headers=headers)
    response.raise_for_status()

    jsonResponse = response.json()

    return jsonResponse

@payment.route('/api/orders', methods=['POST'])
def createOrder():
    try:
        # Validate incoming data
        data = request.json
        if 'cart' not in data:
            raise ValueError("Invalid request format: 'cart' not found in request JSON.")

        # Call the function to create the order
        jsonResponse = create_order(data['cart'])

        return jsonify(jsonResponse)
    except requests.exceptions.RequestException as error:
        print(f"Failed to create order: {error}")
        return jsonify({'error': 'Failed to create order.'}), 500
    except ValueError as error:
        print(f"Invalid request: {error}")
        return jsonify({'error': str(error)}), 400


def register_order():
    # checking if the user is logged in
    if current_user.is_authenticated:
        # bringing all the items inside the cart
        items = Cart.query.filter_by(user=current_user).all()

        # adding proved items to ordered products and change its amount in the stock
        for item in items:
            order = Order.query.filter_by(product_id=item.product_id).first()
            product = Product.query.filter_by(product_id=item.product_id).first()

            # if the order is already exist we increment the quantity of product
            # otherwise register another order
            if order:
                order.amount += item.amount
                product.stock -= item.amount
                product.selled += item.amount
            else:
                order = Order(amount=item.amount, user=current_user, product_id=item.product_id)
                product.stock -= item.amount
                product.selled += item.amount
                db.session.add(order)

            db.session.commit()
    return


@payment.route('/api/orders/<orderID>/capture', methods=['POST'])
def onApprove(orderID):
    try:
        # Call the function to capture the order
        jsonResponse = capture_order(orderID)

        # register the order
        register_order()

        return jsonify(jsonResponse)
    except requests.exceptions.RequestException as error:
        print(f"Failed to capture order: {error}")
        return jsonify({'error': 'Failed to capture order.'}), 500


@payment.route('/checkout')
def checkout():
    # checking if the user is logged in, then retreive its address from database
    if current_user.is_authenticated:
        address = Address.query.filter_by(user=current_user).first()

        # checking if address exist, then passing the data into the form
        # otherwise the form stays empty
        if address:
            form_data = {
                'country': address.country,
                'city': address.city,
                'street': address.street,
                'home': address.home
            }

    return render_template("checkout.html", title="Checkout", form=form_data, PAYPAL_CLIENT_ID=PAYPAL_CLIENT_ID)
