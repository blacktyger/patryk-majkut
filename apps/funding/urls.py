from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('balance', views.balance, name='balance'),
    path('transactions', views.transactions, name='transactions'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
    ]
