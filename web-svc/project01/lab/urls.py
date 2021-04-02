from django.contrib.auth import views
from django.urls import path

from .views import index


app_name = 'lab'

urlpatterns = [
    path('', index, name='home'),
]
