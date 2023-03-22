from django.shortcuts import render

# Create your views here.
from Consumer.EBS_Request import EBSRequestAPIView
from Balance.serializers import *

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
class CardTransferView(EBSRequestAPIView):
    """
    Transfer money from one card to the other.
    This implements the request 3.8 'Card Transfer' in
    the EBS 'Multi-Channel support - Consumer' API documentation.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = CardTransferAPISerializer
    ebs_service_path = 'doCardTransfer'
    transaction_model_class = CardTransferAPISerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # serializer = self.get_serializer(data=request.data)
            # serializer.is_valid(raise_exception=True)
            payload = self.get_payload_from_input(serializer.data)
            self.validated_data = serializer.validated_data
            try:
                print(payload)
                ebs_response = self.ebs_post(payload)
            except requests.exceptions.ConnectionError:
                # logger = self.get_logger()
                url = self.get_ebs_base_url() + '/' + self.get_ebs_service_path()
                Response("Failed to process the EBS request because the connection to VPN is broken. url: %s", url)
                

            return Response(json.loads(ebs_response.text))
        else:
            return Response(serializer.errors)
        
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
            # return Response(payload)
        else:
            return Response(serializer.errors)

class PaymentView(EBSRequestAPIView):
    """
    Send a message to EBS to pay a bill or top up customer account for one of the billers (from Get Bill)
    This implements the request 3.6 'Payment' in
    the EBS 'Multi-Channel support - Consumer' API documentation.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = PaymentConsumerAPISerializerEntity
    ebs_service_path = 'payment'
    # transaction_model_class = PaymentTransaction
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




class changePassword(EBSRequestAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = ChangePasswordSerializer
    ebs_service_path = 'changePassword'
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
        

class forgetPassword(EBSRequestAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = ForgetPasswordSerializer
    ebs_service_path = 'forgetPassword'
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
                ebs_response = self.ebs_post(payload)
            except requests.exceptions.ConnectionError:
                # logger = self.get_logger()
                url = self.get_ebs_base_url() + '/' + self.get_ebs_service_path()
                Response("Failed to process the EBS request because the connection to VPN is broken. url: %s", url)
                

            return Response(json.loads(ebs_response.text))
        else:
            return Response(serializer.errors)
    
    
