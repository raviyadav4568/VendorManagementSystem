from rest_framework import serializers
from .models import PurchaseOrder
import datetime

class Purchase_order_list(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'po_number', 'vendor', 'delivery_date', 'items', 'quantity', 'status', 'issue_date']

    def create(self, validated_data):
        data = PurchaseOrder(**validated_data)
        if data.status == "":
            data.status = 'Pending'
        if data.issue_date == "":
            data.issue_date = datetime.datetime.now()
        data.save()
        return data
    
class Purchase_order_details(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgement_date']
    

    
