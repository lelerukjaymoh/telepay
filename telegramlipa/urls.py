from django.urls import path
from telegramlipa import views
from telegramlipa.views import TransactionsListView

urlpatterns = [
    path('', views.home, name='home'),
    # path('lipaonline', views.lipaonline, name='lipaonline'),
    path('confirmation', views.confirmation, name='confirmation'),
    path('transactions', TransactionsListView.as_view()),
    path('initiatedtransaction', views.initiatedtransaction, name='initiatedtransaction'),
    path('incompletetransaction', views.incompletetransaction, name='incompletetransaction'),
    path('successfultransaction', views.successfultransaction, name='successfultransaction'),
]
