from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Transaction(BaseModel):
    MerchantRequestID = models.CharField(max_length=100)
    CheckoutRequestID = models.CharField(max_length=100)    
    ResultCode = models.IntegerField()    
    ResultDesc = models.CharField(max_length=100)

    def __str__(self):
        return self.MerchantRequestID

