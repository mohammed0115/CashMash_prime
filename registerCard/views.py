from django.shortcuts import render
from Consumer.EBS_Request import EBSRequestAPIView
from rest_framework import generics
from rest_framework.response import Response
from registerCard.serializers import PhysicalCardSerializer,VirtualCardSerializer
import requests
import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from EBS_CONSUMER_API.models import ebs_consumer,ModelPublickey
from django.conf import settings
from .models import *
from rest_framework import generics
from EbsAPIs.views import Ebs
ebs_services=Ebs()

@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def RegisterStandardCard(request):
    """
    #Send a request to EBS to register standard card of specific transaction.
    #This implements the request 3.16 'Transaction Status' in
    #the EBS 'Multi-Channel support - Consumer' API documentation.
    """
    if request.method == 'POST':
        serializer = PhysicalCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            resonse=ebs_services.register_physical_standard(**serializer.data)
            return Response(json.loads(resonse), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def RegisterVirtualCard(request):
    """
    #Send a request to EBS to register standard card of specific transaction.
    #This implements the request 3.16 'Transaction Status' in
    #the EBS 'Multi-Channel support - Consumer' API documentation.
    """
    if request.method == 'POST':
        serializer = VirtualCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            resonse=ebs_services.register_virtual(**serializer.data)
            return Response(json.loads(resonse), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
class RegisterGolenCard(EBSRequestAPIView):
    
    authentication_classes = ()
    permission_classes = ()
    serializer_class = PhysicalCardSerializer
    ebs_service_path = 'register'
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

    def get_response_data(self, ebs_response_content_json):
        ebs_response_content_json = super(RegisterGolenCard, self).get_response_data(ebs_response_content_json)
        if 'originalTransaction' in ebs_response_content_json:
            app_id = ebs_response_content_json['originalTransaction'].get('applicationId')
            if app_id:
                del ebs_response_content_json['originalTransaction']['applicationId']

        return ebs_response_content_json
    

class RegisterGolenCard(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()
    queryset = Register.objects.all()
    # serializer_class = PhysicalCardSerializer
    ebs_service_path = 'register'
    ebs_base_url = settings.EBS_CONSUMER_API["END_POINT"]
    verify_ssl = settings.EBS_CONSUMER_API["VERIFY_SSL"]
    timeout = settings.EBS_CONSUMER_API["TIMEOUT"]
    application_id = settings.EBS_CONSUMER_API["APPLICATION_ID"]
    # ebs_base_url = ebs_consumer.objects.first().END_POINT
    # verify_ssl =ebs_consumer.objects.first().VERIFY_SSL
    # timeout = ebs_consumer.objects.first().TIMEOUT
    # application_id = ebs_consumer.objects.first().APPLICATION_ID
    # @method_decorator()
    def dispatch(self, *args, **kwargs):
        return super(RegisterGolenCard, self).dispatch(*args, **kwargs)
    def get_payload_from_input(self, input_data):
        payload = {}
        payload.update(input_data)
        payload.update({'applicationId': self.application_id})
        # payload.update({'UUID':str(uuid.uuid4())})
        return payload

    def get_response_data(self, ebs_response_content_json):
        ebs_response_content_json.pop('applicationId')
        return ebs_response_content_json
    def post(self, request, format=None):
        serializer = self.get_serializer_class(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            try:
                ebs_response = self.ebs_post(serializer.data)
            except requests.exceptions.ConnectionError:
                # logger = self.get_logger()
                url = self.get_ebs_base_url() + '/' + self.get_ebs_service_path()
                Response("Failed to process the EBS request because the connection to VPN is broken. url: %s", url)
                

            # return Response()
            return Response(json.loads(ebs_response.text), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # # def post(self, request, *args, **kwargs):
    #     serializer = PhysicalCardSerializer(data=request.data)
    #     if serializer.is_valid():
    #         # serializer = self.get_serializer(data=request.data)
    #         # serializer.is_valid(raise_exception=True)
    #         payload = self.get_payload_from_input(serializer.data)
    #         self.validated_data = serializer.validated_data
    #         try:
    #             ebs_response = self.ebs_post(payload)
    #         except requests.exceptions.ConnectionError:
    #             # logger = self.get_logger()
    #             url = self.get_ebs_base_url() + '/' + self.get_ebs_service_path()
    #             Response("Failed to process the EBS request because the connection to VPN is broken. url: %s", url)
                

    #         return Response(json.loads(ebs_response.text))
    #     else:
    #         return Response(serializer.errors)
"""
# class RegisterAgentCard(EBSRequestAPIView):
#     permission_classes = ()
#     authentication_classes = ()
#     serializer_class = PhysicalCardSerializer
#     ebs_service_path  = 'register'
#     # def post(self, request, *args, **kwargs):
#     #     serializer = PhysicalCardSerializer(data=request.data)
#     #     if serializer.is_valid():
#     #         # serializer = self.get_serializer(data=request.data)
#     #         # serializer.is_valid(raise_exception=True)
#     #         payload = self.get_payload_from_input(serializer.data)
#     #         self.validated_data = serializer.validated_data
#     #         try:
#     #             ebs_response = self.ebs_post(payload)
#     #         except requests.exceptions.ConnectionError:
#     #             # logger = self.get_logger()
#     #             url = self.get_ebs_base_url() + '/' + self.get_ebs_service_path()
#     #             Response("Failed to process the EBS request because the connection to VPN is broken. url: %s", url)
                

#     #         return Response(json.loads(ebs_response.text))
#     #     else:
#     #         return Response(serializer.errors)
# class registerSilverCard(EBSRequestAPIView):
#     permission_classes = ()
#     authentication_classes = ()
#     serializer_class = PhysicalCardSerializer
#     ebs_service_path  = 'register'
#     transaction_model_class=Register
#     def post(self, request, *args, **kwargs):
#         serializer =PhysicalCardSerializer(data=request.data)
#         if serializer.is_valid():
#             # serializer = self.get_serializer(data=request.data)
#             # serializer.is_valid(raise_exception=True)
#             payload = self.get_payload_from_input(serializer.data)
#             self.validated_data = serializer.validated_data
#             try:
#                 ebs_response = self.ebs_post(payload)
#             except requests.exceptions.ConnectionError:
#                 # logger = self.get_logger()
#                 url = self.get_ebs_base_url() + '/' + self.get_ebs_service_path()
#                 Response("Failed to process the EBS request because the connection to VPN is broken. url: %s", url)
                

#             return Response(json.loads(ebs_response.text))
#         else:
#             return Response(serializer.errors)
# class VirtualCard(EBSRequestAPIView):
#     permission_classes = ()
#     authentication_classes = ()
#     serializer_class = VirtualCardSerializer
#     ebs_service_path = 'register'
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
           
#             payload = self.get_payload_from_input(serializer.data)
#             self.validated_data = serializer.validated_data
#             try:
#                 ebs_response = self.ebs_post(payload)
#             except requests.exceptions.ConnectionError:
#                 # logger = self.get_logger()
#                 url = self.get_ebs_base_url() + '/' + self.get_ebs_service_path()
#                 Response("Failed to process the EBS request because the connection to VPN is broken. url: %s", url)
                

#             return Response(json.loads(ebs_response.text))
#         else:
#             return Response(serializer.errors)
