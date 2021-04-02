from django.contrib.auth import views
from django.urls import path

from .views import enter_page, index


app_name = 'root'

urlpatterns = [
    path('', enter_page),
    path('index', index, name='home'),
]
