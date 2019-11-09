from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.conf import settings
from telegramlipa.logic import Lipa
from telegramlipa.models import Transaction
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import base64
import pprint

def home(request):
    return render(request, 'home.html', {})

def lipaonline(request):
    base_url = settings.BASE_URL
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = settings.BUSINESS_SHORTCODE
    passkey = settings.PASSKEY
    data_to_encode = Business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')

    lipa = Lipa()
    access_token = lipa.get_token()
    print(access_token)
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": Business_short_code,
        "Password": decode_password,
        "Timestamp": lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": "1",
        "PartyA": "254717771518", 
        "PartyB": Business_short_code,
        "PhoneNumber": "254717771518",  
        "CallBackURL": "https://1771fa89.ngrok.io/confirmation",
        "AccountReference": "Jaymoh",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    pprint.pprint(response.json())
    return HttpResponse()

@csrf_exempt
def confirmation(request):
    response = json.loads(request.body)
    transaction_response = response['Body']['stkCallback']
    
    save_transaction = Transaction(
        MerchantRequestID = transaction_response['MerchantRequestID'],
        CheckoutRequestID = transaction_response['CheckoutRequestID'],
        ResultCode = transaction_response['ResultCode'],
        ResultDesc = transaction_response['ResultDesc']
    )

    save_transaction.save()

    return render(request, 'confirmation.html', {})

class TransactionsListView(ListView):
    model = Transaction
    template_name = 'transactions.html'

