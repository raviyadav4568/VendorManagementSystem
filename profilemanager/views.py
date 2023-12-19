import json
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import VendorProfile, HistoricalPerformanceModel
from .serializer import VendorList, VendorDetails, HistoricalPerformance


def index(request):
    return render(request, 'index.html')

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def vendor_list(request):
    if request.method == 'GET':
        queryset = VendorProfile.objects.all()
        vendor_serializer = VendorList(queryset, many=True)
        return Response(vendor_serializer.data)
    elif request.method == 'POST':
        data = VendorList(data=request.data)
        data.is_valid(raise_exception=True)
        data.validated_data
        data.save()
        insert = data.initial_data
        historical_performance_create = HistoricalPerformanceModel(vendor_id=insert['vendor_code'])
        historical_performance_create.save()
        return Response(data.data)

@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def vendor_detail(request, vendor_code):
    vendors_object = get_object_or_404(VendorProfile, vendor_code=vendor_code)
    invalid_request_msg = "Invalid Request Body"
    if request.method == "PUT" or request.method == "PATCH":
        if request.body is not None:
            try:
                data = json.loads(request.body)
            except:
                return Response(invalid_request_msg, status=status.HTTP_400_BAD_REQUEST)
            all_fields = [f.name for f in vendors_object._meta.fields]
            if len(data) != 0:
                for keys in data.keys():
                    if keys not in all_fields:
                        return Response("Field names in the request body are not proper", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(invalid_request_msg, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        vendors_serializer = VendorDetails(vendors_object)
        return Response(vendors_serializer.data)
    elif request.method == 'PUT':
        data = VendorDetails(vendors_object, data=request.data)
        data.is_valid(raise_exception=True)
        data.validated_data
        data.save()
        return Response(data.data, status=status.HTTP_201_CREATED)
    elif request.method == 'PATCH':
        data = VendorDetails(vendors_object, data=request.data, partial=True)
        data.is_valid(raise_exception=True)
        data.validated_data
        data.save()
        return Response(data.data)
    elif request.method == 'DELETE':
        vendors_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view()    
@permission_classes([IsAuthenticated])
def performance(request, vendor_code):
    queryset = VendorProfile.objects.all()
    vendor_list = [int(i.vendor_code) for i in list(queryset)]
    if vendor_code not in vendor_list:
        return Response("Vendor not found, check the vendor_code", status=status.HTTP_404_NOT_FOUND)
    historical_performance = HistoricalPerformanceModel.objects.filter(vendor_id=vendor_code).first()
    historical_performance_serializer = HistoricalPerformance(historical_performance)
    return Response(historical_performance_serializer.data)

