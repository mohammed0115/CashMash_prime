from django.shortcuts import render
from Consumer.EBS_Request import EBSRequestAPIView
from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
import json
class RegisterGolenCard(EBSRequestAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = GoldenCardSerializer
    ebs_service_path = 'register'
class RegisterAgentCard(EBSRequestAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = GoldenCardSerializer
    ebs_service_path = 'register'
class registerSilverCard(EBSRequestAPIView):
    permission_classes = ()
    authentication_classes = ()
    queryset = Register.objects.all()
    serializer_class = SilverCardSerializer
    ebs_service_path = 'register'
class VirtualCard(EBSRequestAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = VirtualCardSerializer
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
class RegisterList(generics.ListAPIView):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer