from django.urls import path, include
# from .views import create, delete


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    # path('create', create),
    # path('delete', delete),
]
