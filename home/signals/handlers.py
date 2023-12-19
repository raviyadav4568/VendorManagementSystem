import datetime
from django.conf import settings
from django.db.models.signals import post_save
from django.db.models import Avg, F
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from purchaseordertracking.signals import purchase_order_updated, purchase_order_acknowledge
from purchaseordertracking.models import PurchaseOrder
from profilemanager.models import VendorProfile, HistoricalPerformanceModel

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(signal=purchase_order_updated)
def calculate_fulfillment_rate(sender, **kwargs):
    data_for_check = kwargs['data_for_check']
    vendor_id = kwargs['vendor_id']
    if "status" in data_for_check.keys():
        completed_count = PurchaseOrder.objects.filter(vendor_id=vendor_id, status='completed').count()
        total_count = PurchaseOrder.objects.filter(vendor_id=vendor_id).count()
        try:
            fulfillment_rate = round(completed_count/total_count, 3)
        except ZeroDivisionError:
            return Response("Total count for Vendor is zero hence calculation cannot be performed due to zero division error. ")
        VendorProfile.objects.filter(vendor_code=vendor_id).update(fulfillment_rate=fulfillment_rate)
        HistoricalPerformanceModel.objects.filter(vendor_id=vendor_id).update(fulfillment_rate=fulfillment_rate, date=datetime.datetime.now())

        if data_for_check['status'] == 'completed':
            on_time_po = PurchaseOrder.objects.filter(vendor_id=vendor_id).filter(delivery_date__gte=datetime.datetime.now()).count()
            try:
                on_time_delivery_rate = round(on_time_po / total_count, 3)
            except ZeroDivisionError:
                return Response("Total count for Vendor is zero hence calculation cannot be performed due to zero division error. ")
            VendorProfile.objects.filter(vendor_code=vendor_id).update(on_time_delivery_rate=on_time_delivery_rate) 
            HistoricalPerformanceModel.objects.filter(vendor_id=vendor_id).update(on_time_delivery_rate=on_time_delivery_rate, date=datetime.datetime.now())

    if "quality_rating" in data_for_check.keys():
        is_completed = PurchaseOrder.objects.filter(po_number=kwargs['po_number']).first()
        if is_completed.status == 'completed':
            quality_rating = PurchaseOrder.objects.filter(vendor=vendor_id).aggregate(Avg('quality_rating'))
            quality_rating_avg = round(quality_rating['quality_rating__avg'], 3)
            VendorProfile.objects.filter(vendor_code=vendor_id).update(quality_rating_avg=quality_rating_avg)     
            HistoricalPerformanceModel.objects.filter(vendor_id=vendor_id).update(quality_rating_avg=quality_rating_avg, date=datetime.datetime.now())

@receiver(signal=purchase_order_acknowledge)
def on_purchase_order_acknowledge(sender, **kwargs):
    vendor_id = kwargs['vendor_id']
    queryset = PurchaseOrder.objects.filter(vendor_id=vendor_id).annotate(datediff=F('acknowledgement_date')-F('issue_date')).aggregate(Avg('datediff'))
    datediff = queryset['datediff__avg']
    try:
        calculated_datediff = round(datediff.days + ((datediff.seconds/3600)/24), 3)
    except ZeroDivisionError:
        return Response("Cannot divide by zero")
    VendorProfile.objects.filter(vendor_code=vendor_id).update(average_response_time=calculated_datediff)
    HistoricalPerformanceModel.objects.filter(vendor_id=vendor_id).update(average_response_time=calculated_datediff, date=datetime.datetime.now())
    