from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
    ]
