from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction

# signup forms  
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from telegramlipa.forms import ProfileUpdateForm

from django.conf import settings
from telegramlipa.logic import Lipa
from telegramlipa.models import Transaction, Profile
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import base64
import pprint

def home(request):
    print(request.user.id)
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
            "TransactionDesc": "Channel join payment"
        }
        response = requests.post(api_url, json=request, headers=headers)
        pprint.pprint(response.json())

        return HttpResponse('')

    return render(request, 'home.html', {})

@csrf_exempt
def confirmation(request):
    print(request.method)
    print(request.body)
    # if request.method == 'POST':

    #     print(request.method)

    #     response = json.loads(request.body)
    #     pprint.pprint(response)
    #     transaction_response = response['Body']['stkCallback']

    #     transaction_result = transaction_response['ResultCode']
    #     print("ResultCode = %s" % transaction_result)
    #     print(type(transaction_result))

    return render(request, 'incompletetransaction.html', {})
    

def successfultransaction(request):
    return render(request, 'successfultransaction.html', {})  

def initiatedtransaction(request):
    return render(request, 'initiatedtransaction.html', {})

def incompletetransaction(request):
    return render(request, 'incompletetransaction.html')


# Dashboard views

@login_required
def dashboard(request):

    # REVIEW => Check if user has completed registration.

    account = Profile.objects.get(user=request.user)
    if account.telegram_channel_name:
        print(account.telegram_channel_name)
         
    return render(request, 'client/dashboard/dashboard.html', {})

class ProfileUpdateView(CreateView):
    model = Profile
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('login')
    template_name = 'client/dashboard/update_account.html'

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)

# REVIEW TO BE REVIEWD => Either to use seperate file to tackle auth system

# signup 
class Signup(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class TransactionsListView(ListView):
    model = Transaction
    template_name = 'transactions.html'

