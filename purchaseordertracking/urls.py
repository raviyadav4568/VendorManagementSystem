from django.urls import path, include
from . import views

urlpatterns = [

    path('purchase_orders', views.purchase_order_list),
    path('purchase_orders/<int:po_number>', views.purchase_order_detail),
    path('purchase_orders/<int:po_number>/acknowledge', views.acknowledge)

        
]