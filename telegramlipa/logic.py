from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth

class Lipa:
    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET
 
    def get_token(self):
        token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

        response = requests.get(token_url, auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret))
        return response.json()['access_token']
