from django.urls import path
from telegramlipa import views
from telegramlipa.views import TransactionsListView, Signup, ProfileUpdateView

urlpatterns = [
    path('', views.home, name='home'),
    # path('lipaonline', views.lipaonline, name='lipaonline'),
    path('confirmation', views.confirmation, name='confirmation'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/update', views.ProfileUpdateView.as_view(), name='update'),
    path('transactions', views.TransactionsListView.as_view()),
    path('initiatedtransaction', views.initiatedtransaction, name='initiatedtransaction'),
    path('incompletetransaction', views.incompletetransaction, name='incompletetransaction'),
    path('successfultransaction', views.successfultransaction, name='successfultransaction'),
    path('accounts/signup', views.Signup.as_view(), name='signup'),
]
