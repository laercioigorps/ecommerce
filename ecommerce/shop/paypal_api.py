import os

import requests
from requests.auth import HTTPBasicAuth

CLIENT_ID = os.getenv(
    "PAYPAL_CLIENT_ID",
    "AcEVIaO09V6fwCw-zwIGA3jY9K19M5bJi8mQ3odiOB_fpkym2OSw3gSHwfKJYWM1vfWxgE4aecSn3OAB",
)
APP_SECRETE = os.getenv(
    "PAYPAL_APP_SECRET",
    "EJcNRP9yfMPNAR8Ux3AuVn6LQYMBJNMoYJZ4XKB4i5ztg5944fMV6oLjUgy1od0XrD3tLXhInUjTA8BJ",
)
base = "https://api-m.sandbox.paypal.com"


def generate_access_token():
    data = "grant_type=client_credentials"
    response = requests.post(
        f"{base}/v1/oauth2/token",
        headers={"Accept": "application/json", "Accept-Language": "en_US"},
        auth=HTTPBasicAuth(CLIENT_ID, APP_SECRETE),
        data=data,
    )
    oauth_body_json = response.json()
    access_token = oauth_body_json["access_token"]
    return access_token


def generateClientToken():
    access_token = generate_access_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
        "Accept-Language": "en_US",
    }
    response = requests.post(
        f"{base}/v1/identity/generate-token",
        headers=headers,
    )
    response_json = response.json()
    client_token = response_json["client_token"]
    return client_token


def create_order(total):
    access_token = generate_access_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
    }
    data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "description": "online shopping",
                "amount": {
                    "currency_code": "USD",
                    "value": round(float(total), 2),
                },
            }
        ],
    }

    response = requests.post(
        "https://api-m.sandbox.paypal.com/v2/checkout/orders",
        headers=headers,
        json=data,
    )
    print(response.json())
    return response


def capture_order(order_id):
    access_token = generate_access_token()
    url = f"{base}/v2/checkout/orders/{order_id}/capture"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
    }
    response = requests.post(
        url,
        headers=headers,
    )
    print(response.json())
    return response
