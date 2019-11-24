from django.test import TestCase

from django.test import Client
c = Client()
response = c.post(path='/confirmation',
                  data={
                      'Body': {
                          'stkCallback': {
                              'MerchantRequestID': '3044-524685-1',
                              'CheckoutRequestID': 'ws_CO_131120192004130984',
                              'ResultCode': 1,
                              'ResultDesc': 'The balance is insufficient for the transaction'}}},
                  content_type='application/json;charset=UTF-8')