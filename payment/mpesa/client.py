import base64
import requests
from django.conf import settings
from datetime import datetime


class MpesaClient:
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.passkey = settings.MPESA_PASSKEY
        self.business_shortcode = settings.MPESA_SHORTCODE
        self.api_base_url = settings.MPESA_API_BASE_URL
        self.token_url = f"{self.api_base_url}/oauth/v1/generate?grant_type=client_credentials"
        self.stk_push_url = f"{self.api_base_url}/mpesa/stkpush/v1/processrequest"
        self.callback_url = settings.MPESA_CALLBACK_URL

    def get_access_token(self):
        response = requests.get(
            self.token_url,
            auth=(self.consumer_key, self.consumer_secret)
        )
        response.raise_for_status()
        return response.json()['access_token']

    def generate_password(self, timestamp):
        data_to_encode = self.business_shortcode + self.passkey + timestamp
        encoded = base64.b64encode(data_to_encode.encode())
        return encoded.decode('utf-8')

    def stk_push(self, phone_number, amount, account_reference="OSHEN", transaction_desc="Order Payment"):
        # Format phone number to international
        if phone_number.startswith("0"):
            phone_number = "254" + phone_number[1:]

        access_token = self.get_access_token()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = self.generate_password(timestamp)

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "BusinessShortCode": self.business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": self.business_shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc,
        }

        try:
            response = requests.post(self.stk_push_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print("💥 STK Push Error:")
            print("Status Code:", response.status_code)
            print("Response Text:", response.text)
            raise e
