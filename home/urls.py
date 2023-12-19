from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('', views.welcome),
    path('create_user', views.create_user),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]