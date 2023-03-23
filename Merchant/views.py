from django.shortcuts import render
from Merchant.serializers import *
# Create your views here.
from Consumer.EBS_Request import EBSRequestAPIView
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re
import requests
import datetime
import uuid

import json
import time


class doQRRefund(EBSRequestAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = QRRefundSerializer
    ebs_service_path = 'doQRRefund'
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # serializer = self.get_serializer(data=request.data)
            # serializer.is_valid(raise_exception=True)
            payload = self.get_payload_from_input(serializer.data)
            self.validated_data = serializer.validated_data
            try:
                payload.update({'applicationId': 'ITQAN'})
                ebs_response = self.ebs_post(payload)
            except requests.exceptions.ConnectionError:
                # logger = self.get_logger()
                url = self.get_ebs_base_url() + '/' + self.get_ebs_service_path()
                Response("Failed to process the EBS request because the connection to VPN is broken. url: %s", url)
                

            return Response(json.loads(ebs_response.text))
        else:
            return Response(serializer.errors)
class doQRPurchase(EBSRequestAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = QRPurchaseSerializer
    ebs_service_path = 'doQRPurchase'
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # serializer = self.get_serializer(data=request.data)
            # serializer.is_valid(raise_exception=True)
            payload = self.get_payload_from_input(serializer.data)
            self.validated_data = serializer.validated_data
            try:
                payload.update({'applicationId': 'ITQAN'})
                ebs_response = self.ebs_post(payload)
            except requests.exceptions.ConnectionError:
                # logger = self.get_logger()
                url = self.get_ebs_base_url() + '/' + self.get_ebs_service_path()
                Response("Failed to process the EBS request because the connection to VPN is broken. url: %s", url)
                

            return Response(json.loads(ebs_response.text))
        else:
            return Response(serializer.errors)    
    
    

class RequestPinChangeView(EBSRequestAPIView):
    """
    Request to change the IPIN for a card.
    This implements the request 3.10 'Change IPIN' in
    the EBS 'Multi-Channel support - Consumer' API documentation.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = ChangeCardsIpin
    ebs_service_path = 'changeIPin'
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # serializer = self.get_serializer(data=request.data)
            # serializer.is_valid(raise_exception=True)
            payload = self.get_payload_from_input(serializer.data)
            self.validated_data = serializer.validated_data
            try:
                payload.update({'applicationId': 'ITQAN'})
                ebs_response = self.ebs_post(payload)
            except requests.exceptions.ConnectionError:
                # logger = self.get_logger()
                url = self.get_ebs_base_url() + '/' + self.get_ebs_service_path()
                Response("Failed to process the EBS request because the connection to VPN is broken. url: %s", url)
                

            return Response(json.loads(ebs_response.text))
        else:
            return Response(serializer.errors) 