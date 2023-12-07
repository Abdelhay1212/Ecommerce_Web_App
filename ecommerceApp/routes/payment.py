import json
import base64
import requests
from flask import request, jsonify, Blueprint, render_template
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

    url = f'{BASE_URL}/v2/checkout/orders'
    payload = {
        'intent': "CAPTURE",
        'purchase_units': [
            {
                'amount': {
                    'currency_code': "USD",
                    'value': "100.00",
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

    return {
        'jsonResponse': jsonResponse,
        'httpStatusCode': response.status_code
    }


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

    return {
        'jsonResponse': jsonResponse,
        'httpStatusCode': response.status_code
    }


@payment.route('/api/orders', methods=['POST'])
def createOrder():
    try:
        # Validate incoming data
        data = request.json
        if 'cart' not in data:
            raise ValueError("Invalid request format: 'cart' not found in request JSON.")

        # Call the function to create the order
        jsonResponse, httpStatusCode = create_order(data['cart'])

        return jsonify(jsonResponse)
    except requests.exceptions.RequestException as error:
        print(f"Failed to create order: {error}")
        return jsonify({'error': 'Failed to create order.'}), 500
    except ValueError as error:
        print(f"Invalid request: {error}")
        return jsonify({'error': str(error)}), 400


@payment.route('/api/orders/<orderID>/capture', methods=['POST'])
def onApprove(orderID):
    try:
        # Call the function to capture the order
        jsonResponse, httpStatusCode = capture_order(orderID)

        return jsonify(jsonResponse)
    except requests.exceptions.RequestException as error:
        print(f"Failed to capture order: {error}")
        return jsonify({'error': 'Failed to capture order.'}), 500


@payment.route('/checkout')
def checkout():
    return render_template("checkout.html", PAYPAL_CLIENT_ID=PAYPAL_CLIENT_ID)
