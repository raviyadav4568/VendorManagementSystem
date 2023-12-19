from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Vendor Management Admin'
admin.site.index_title = 'Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('profilemanager/', include('profilemanager.urls')),
    path('purchase_order_tracking/', include('purchaseordertracking.urls')),
]
