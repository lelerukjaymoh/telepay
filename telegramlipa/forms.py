from django import forms
from telegramlipa.models import Profile 


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['telegram_channel_name', 'phone', 'email',
                  'billing_package']
