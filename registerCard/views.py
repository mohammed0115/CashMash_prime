from django.shortcuts import render
from Consumer.EBS_Request import EBSRequestAPIView
from rest_framework import generics
from .serializers import *
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


class RegisterList(generics.ListAPIView):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer