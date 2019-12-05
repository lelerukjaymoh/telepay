from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractUser):
    have_completed_profile = models.BooleanField(default=False)


class Transaction(BaseModel):
    MerchantRequestID = models.CharField(max_length=100)
    CheckoutRequestID = models.CharField(max_length=100)
    ResultCode = models.IntegerField()
    ResultDesc = models.CharField(max_length=100)

    def __str__(self):
        return self.MerchantRequestID


class Profile(models.Model):
    BILLING_PACKAGES_CHOICES = [
        ('GOLD', 'Gold'),
        ('SILVER', 'Silver'),
        ('BRONZE', 'Bronze'),
    ]
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user')
    url = models.SlugField(max_length=100)
    telegram_channel_name = models.CharField(max_length=100)
    phone = models.IntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    billing_package = models.CharField(
        max_length=100, choices=BILLING_PACKAGES_CHOICES, default='BRONZE')
    have_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.telegram_channel_name

    def save(self, *args, **kwargs):
        if not self.id:
            self.url = slugify(self.telegram_channel_name)

        super(Profile, self).save(*args, **kwargs)

    def update_profile_completio_status(self):
        status = self.user
        status.have_completed_profile = True
        status.save()

class TelegramSubscribers:
    username = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username
