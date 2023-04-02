from django.shortcuts import render
from rest_framework.response import Response
import requests
import json
import datetime
import uuid
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from IpinGeneration.serializers import doGenerateIPinRequestSerializer,doGenerateCompletionIPinRequestSerializer
from rest_framework import status
EBS_CONSUMER_API = {
    'END_POINT': 'https://172.16.199.1:8877/IPinGeneration',
    'APPLICATION_ID': 'ITQAN',
    'VERIFY_SSL': False,  # See line EBS_MERCHANT_API.VERIFY_SSL.
    'TIMEOUT': 60,  # 60 seconds
    'TIME_ZONE': 'Africa/Khartoum'  # This is used to parse datetime to the time zone EBS required
}
def post(servicename,data):
    resp = json.loads(requests.post(EBS_CONSUMER_API["END_POINT"]+f"/{servicename}", json=data, verify=False).text)
    return Response(resp) 

@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def get_public_key(request):
        # response = base_response
        data = {}
        data["userName"] = "ITQAN"
        data["UUID"] = str(uuid.uuid4())
        data["tranDateTime"] = datetime.datetime.now().strftime("%d%m%y%H%M%S")
        
        # resp = json.loads(requests.post(EBS_CONSUMER_API["END_POINT"]+ "/getPublicKey", json=data, verify=False).text)
      
        return post("getPublicKey",data) 

@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def doGenerateIPinRequest(request):
    """
    #doGenerateIPinRequest
    """
    if request.method == 'POST':
        serializer = doGenerateIPinRequestSerializer(data=request.data)
        if serializer.is_valid():
           return post("doGenerateIPinRequest",serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@authentication_classes(())
@permission_classes(())   
def doGenerateCompletionIPinRequest(request):
    """
    #doGenerateIPinRequest
    """
    if request.method == 'POST':
        serializer = doGenerateCompletionIPinRequestSerializer(data=request.data)
        if serializer.is_valid():
           return post("doGenerateCompletionIPinRequest",serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)