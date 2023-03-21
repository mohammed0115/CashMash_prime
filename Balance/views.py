from django.shortcuts import render

# Create your views here.
from Consumer.EBS_Request import EBSRequestAPIView
from Consumer.serializers import BalanceInqueryAPISerializer,BillInquiryConsumerAPISerializer

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

class BalanceInquiryView(EBSRequestAPIView):
    """
    Request card balance.
    This implements the request 3.9 'Balance Inquiry' in
    the EBS 'Multi-Channel support - Consumer' API documentation.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = BalanceInqueryAPISerializer
    ebs_service_path = 'getBalance'
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            payload = self.get_payload_from_input(serializer.data)
            self.validated_data = serializer.validated_data
            try:
                ebs_response = self.ebs_post(payload)
            except requests.exceptions.ConnectionError:
                # logger = self.get_logger()
                url = self.get_ebs_base_url() + '/' + self.get_ebs_service_path()
                Response("Failed to process the EBS request because the connection to VPN is broken. url: %s", url)
                

            return Response(json.loads(ebs_response.text))
        else:
            return Response(serializer.errors)
        
class GetBill(EBSRequestAPIView):
    """
    Send a message to EBS to get bill information for a specific customer accounts.
    This implements the request 3.5 'Bill Inquiry' in
    the EBS 'Multi-Channel support - Consumer' API documentation.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = BillInquiryConsumerAPISerializer
    ebs_service_path = 'getBill'
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # serializer = self.get_serializer(data=request.data)
            # serializer.is_valid(raise_exception=True)
            payload = self.get_payload_from_input(serializer.data)
            self.validated_data = serializer.validated_data
            try:
                ebs_response = self.ebs_post(payload)
            except requests.exceptions.ConnectionError:
                # logger = self.get_logger()
                url = self.get_ebs_base_url() + '/' + self.get_ebs_service_path()
                Response("Failed to process the EBS request because the connection to VPN is broken. url: %s", url)
                

            return Response(json.loads(ebs_response.text))
        else:
            return Response(serializer.errors)