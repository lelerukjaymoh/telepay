from django import forms
from telegramlipa.models import Profile 

from django.contrib.auth import get_user_model
User = get_user_model()



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['telegram_channel_name', 'phone', 'email',
                  'billing_package']
