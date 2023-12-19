from django.db import models
from profilemanager.models import VendorProfile

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=255)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=255)
    quality_rating = models.FloatField(max_length=255, null=True)
    issue_date = models.DateTimeField()
    acknowledgement_date = models.DateTimeField(null=True)