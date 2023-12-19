from rest_framework import serializers
from .models import VendorProfile, HistoricalPerformanceModel

class VendorList(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = ['vendor_code','name', 'vendor_code', 'contact_details', 'address']

    
class VendorDetails(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = ['vendor_code','name', 'vendor_code', 'contact_details', 'address']

class HistoricalPerformance(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformanceModel
        fields = ['vendor_id', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
    
    

    
