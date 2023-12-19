from django.db import models

class VendorProfile(models.Model):
    name = models.CharField(max_length=255, blank=False)
    contact_details = models.TextField(max_length=255, blank=False)
    address = models.CharField(max_length=255, blank=False)
    vendor_code = models.CharField(primary_key=True, max_length=32, blank=False)
    on_time_delivery_rate = models.FloatField(max_length=32, null=True)
    quality_rating_avg = models.FloatField(max_length=32, null=True)
    average_response_time = models.FloatField(max_length=32, null=True)
    fulfillment_rate = models.FloatField(max_length=16, null=True)

class HistoricalPerformanceModel(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    on_time_delivery_rate = models.FloatField(max_length=32, null=True)
    quality_rating_avg = models.FloatField(max_length=32, null=True)
    average_response_time = models.FloatField(max_length=32, null=True)
    fulfillment_rate = models.FloatField(max_length=16, null=True)