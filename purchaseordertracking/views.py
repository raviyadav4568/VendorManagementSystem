import datetime, json
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from .models import PurchaseOrder
from .serializer import Purchase_order_list, Purchase_order_details
from .signals import purchase_order_updated, purchase_order_acknowledge


def index(request):
    return render(request, 'index.html')

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def purchase_order_list(request):
    if request.method == 'GET':
        queryset = PurchaseOrder.objects.all()
        vendor = request.query_params.get('vendor')
        if vendor is not None:
            queryset=queryset.filter(vendor=vendor)
        purchase_order_serializer = Purchase_order_list(queryset, many=True)
        return Response(purchase_order_serializer.data)
    elif request.method == 'POST':
        data = Purchase_order_list(data=request.data)
        data.is_valid(raise_exception=True)
        data.validated_data
        data.save()
        return Response(data.data, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def purchase_order_detail(request, po_number):
    purchase_order_object = get_object_or_404(PurchaseOrder, po_number=po_number)
    invalid_request_msg = "Invalid Request Body"
    if request.method == "PUT" or request.method == "PATCH":
        if request.body is not None:
            try:
                data = json.loads(request.body)
            except:
                return Response(invalid_request_msg, status=status.HTTP_400_BAD_REQUEST)
            all_fields = [f.name for f in purchase_order_object._meta.fields]
            if len(data) != 0:
                for keys in data.keys():
                    if keys not in all_fields:
                        return Response("Field names in the request body are not proper", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(invalid_request_msg, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        purchase_order_serializer = Purchase_order_details(purchase_order_object)
        return Response(purchase_order_serializer.data)
    elif request.method == 'PUT':
        data = Purchase_order_details(purchase_order_object, data=request.data)
        data.is_valid(raise_exception=True)
        data.validated_data
        data.save()
        return Response(data.data)
    elif request.method == 'PATCH':
        vendor_id = purchase_order_object.vendor_id
        data = Purchase_order_details(purchase_order_object, data=request.data, partial=True)
        data.is_valid(raise_exception=True)
        data_for_check = data.validated_data
        data.validated_data
        data.save()
        purchase_order_updated.send_robust(sender=purchase_order_detail, data_for_check=data_for_check, vendor_id=vendor_id, po_number=po_number)
        return Response(data.data)
    elif request.method == 'DELETE':
        purchase_order_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def acknowledge(request, po_number):
    purchase_order_object = get_object_or_404(PurchaseOrder, po_number=po_number)
    vendor_id = purchase_order_object.vendor_id
    if request.method == "GET":
        purchase_order_object.acknowledgement_date = datetime.datetime.now()
    elif request.method == "POST":
        request_body_error = "Provide 'date' in body of the request"
        if len(request.body) > 0:
            try:
                data = json.loads(request.body)
            except:
                return Response("Invalid Request Body", status=status.HTTP_400_BAD_REQUEST)
            if "date" not in data.keys():
                return Response(request_body_error, status=status.HTTP_400_BAD_REQUEST)
            else:
                entered_date = datetime.datetime.strptime(data['date'], "%Y-%m-%d")
                entered_day = entered_date.day
                if entered_day == datetime.datetime.now().day:
                    entered_date = datetime.datetime.now()
                elif entered_day - purchase_order_object.issue_date.day < 0:
                    return Response("Acknowledgement date should be greater then Issue date")
                purchase_order_object.acknowledgement_date = entered_date
        else:
            return Response(request_body_error, status=status.HTTP_400_BAD_REQUEST)

    purchase_order_object.save()
    purchase_order_acknowledge.send_robust(sender=acknowledge, vendor_id=vendor_id)
    return Response("Acknowledgement date : "  + str(purchase_order_object.acknowledgement_date))