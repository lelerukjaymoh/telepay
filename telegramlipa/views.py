from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.contrib import messages
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
    if request.method == 'POST':
        messages.add_message(request, messages.SUCCESS, 'Transaction Intited Successfully. Enter PIN on your phone')
        
        phone_no = request.POST['client_phone'][1:]

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
            "PartyA": "254"+phone_no, 
            "PartyB": Business_short_code,
            "PhoneNumber": "254"+phone_no,  
            "CallBackURL": base_url+"/confirmation",
            "AccountReference": "Jaymoh",
            "TransactionDesc": "Leonet Channel join payment"
        }
        response = requests.post(api_url, json=request, headers=headers)
        pprint.pprint(response.json())

        rendered = render_to_string('initiatedtransaction.html', {})
        response = HttpResponse(rendered)

        return response

    return render(request, 'home.html', {})

@csrf_exempt
def confirmation(request):
    if request.method == 'POST':
        response = json.loads(request.body)
        pprint.pprint(response)
        transaction_response = response['Body']['stkCallback']
        
        save_transaction = Transaction(
            MerchantRequestID = transaction_response['MerchantRequestID'],
            CheckoutRequestID = transaction_response['CheckoutRequestID'],
            ResultCode = transaction_response['ResultCode'],
            ResultDesc = transaction_response['ResultDesc']
        )

        save_transaction.save()

        transaction_result = transaction_response['ResultCode']
        print(transaction_result)

        if transaction_response['ResultCode'] != 0:
            print('Transaction successful')

            redirect('incompletetransaction')

        else:
            redirect('home')

   

def initiatedtransaction(request):
    return render(request, 'initiatedtransaction.html', {})

def incompletetransaction(request):
    return render(request, 'incompletetransaction.html')

class TransactionsListView(ListView):
    model = Transaction
    template_name = 'transactions.html'

