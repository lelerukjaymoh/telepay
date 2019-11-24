from django import forms
from telegramlipa.models import Profile 


# class MyModelForm(forms.ModelForm):
#    def __init__(self, *args, **kwargs):
#        self.request = kwargs.pop('request', None)
#        return super().__init__(*args, **kwargs)

#    def save(self, *args, **kwargs):
#        kwargs['commit'] = False
#        obj = super(MyModelForm, self).save(*args, **kwargs)
#        if self.request:
#            obj.user = self.request.user
#        obj.save()
#        return obj

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['telegram_channel_name', 'phone', 'email',
                  'billing_package']
