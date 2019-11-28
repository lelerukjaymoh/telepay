from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib import admin
from telegramlipa.models import Transaction, Profile, User

admin.site.register(Transaction)
admin.site.register(Profile)
admin.site.register(User)
