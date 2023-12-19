from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index),
    path('vendors', views.vendor_list),
    path('vendors/<int:vendor_code>', views.vendor_detail),
    path('vendors/<int:vendor_code>/performance', views.performance)

    
    
]