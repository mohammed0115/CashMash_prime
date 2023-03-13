from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from EBS_CONSUMER_API.models import ebs_consumer
import uuid
from django.conf import settings
from rest_framework import views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
import requests
import logging
import json
import re

sensitive_info_reg = re.compile(',?\s?"(expDate|PAN|PIN|IPIN|newIPIN|userPassword|newUserPassword)": ".*?",?\s?')


class BaseEBSAPIView(views.APIView):
    ebs_base_url = ''
    ebs_service_path = ''
    timeout = None
    serializer_class = None
    verify_ssl = True
    validated_data = None
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            payload = self.get_payload_from_input(serializer.data)
            self.validated_data = serializer.validated_data
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            try:
                ebs_response = self.ebs_post(payload)
            except requests.exceptions.ConnectionError:
                url = self.ebs_base_url() + '/' + self.ebs_service_path()
                raise f"Failed to process the EBS request because the connection to VPN is broken. url: {url}"
            return self.handle_ebs_response(ebs_response)
        else:
            return Response(serializer.errors)

    # def post(self,request, *args, **kwargs):
        
    #     Url=self.ebs_base_url+"/"+self.ebs_service_path
    #     try:
    #         request=requests.post(Url, json=kwargs, verify=False)
    #         if request.status_code==200:
    #             return Response ( json.loads(request.text))
    #         else:
    #             raise "Failed to process the EBS request."
    #     except requests.exceptions.ConnectionError:
    #         url = self.ebs_base_url() + '/' + self.ebs_service_path()
    #         raise f"Failed to process the EBS request because the connection to VPN is broken. url: {url}"
       

    def handle_ebs_response(self, ebs_response):
        if ebs_response.status_code == 200:
            ebs_response_json = ebs_response.json()
            new_ebs_response_json = self.pre_handle_200_ebs_response(ebs_response_json)
            return self.handle_200_ebs_response(new_ebs_response_json)
        else:
            url = getattr(ebs_response, "url", None)
            status_code = getattr(ebs_response, "status_code", None)
            response_data = self._remove_sensitive_info(getattr(ebs_response, "text", None))
            request = getattr(ebs_response, "request", None)
            if request and hasattr(request, 'body') and request.body:
                request_data = self._remove_sensitive_info(request.body.decode('utf-8'))
            else:
                request_data = None
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def pre_handle_200_ebs_response(self, ebs_response_json):
        return ebs_response_json

    def handle_200_ebs_response(self, ebs_response_json):
        self.is_ebs_200_response_successful(ebs_response_json, raise_exception=True)
        response_data = self.get_response_data(ebs_response_json)
        return Response(response_data, status=status.HTTP_200_OK)

    def is_ebs_200_response_successful(self, ebs_response_json, raise_exception=False):
        if str(ebs_response_json['responseCode']) != '0':
            url = self.ebs_base_url + '/' + self.ebs_service_path
            # status_code = 200
            response_data = self._remove_sensitive_info(json.dumps(ebs_response_json))
            if hasattr(self, 'request') and hasattr(self.request, 'data')and self.request.data:
                request_data = self._remove_sensitive_info(json.dumps(self.request.data))
            else:
                request_data = None
            if raise_exception:
                raise ValidationError({"EBS_error": [ebs_response_json.get('responseMessage', '')]},
                                      code=ebs_response_json['responseCode'])
            else:
                return False
        else:
            # status_code = 0
            response_data = self._remove_sensitive_info(json.dumps(ebs_response_json))
            url = self.ebs_base_url + '/' + self.ebs_service_path
            if self.request.data:
                request_data = self._remove_sensitive_info(json.dumps(self.request.data))
            else:
                request_data= None
            return True

    def get_response_data(self, ebs_response_content_json):
        return ebs_response_content_json

    def get_payload_from_input(self, input_data):
        return input_data

    def ebs_post(self, payload):
        ebs_base_url = self.get_ebs_base_url()
        ebs_service_path = self.get_ebs_service_path()
        if not ebs_base_url.endswith('/'):
            ebs_base_url += '/'
        url = ebs_base_url + ebs_service_path
        print(payload)
        ebs_response = requests.post(url=url, json=payload, timeout=self.get_timeout(), verify=self.verify_ssl)    
        return ebs_response

    def get_ebs_base_url(self):
        if self.ebs_base_url:
            return self.ebs_base_url
        else:
            raise AttributeError("base_url is not defined")

    def get_timeout(self):
        if self.timeout:
            return self.timeout
        else:
            raise AttributeError("timeout is not defined")

    def get_ebs_service_path(self):
        if self.ebs_service_path:
            return self.ebs_service_path
        else:
            raise AttributeError("service_url is not defined")

    def get_serializer_class(self):
        if self.serializer_class:
            return self.serializer_class
        else:
            raise AttributeError("serializer_class is not defined")

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'view': self,
        }

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input and serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class

    
    def _remove_sensitive_info(self, message):
        if message:
            return sensitive_info_reg.sub('', message)
        else:
            return message
        
        
        
class EBSRequestAPIView(BaseEBSAPIView):
    # ebs_base_url = settings.EBS_CONSUMER_API["END_POINT"]
    # verify_ssl = settings.EBS_CONSUMER_API["VERIFY_SSL"]
    # timeout = settings.EBS_CONSUMER_API["TIMEOUT"]
    # application_id = settings.EBS_CONSUMER_API["APPLICATION_ID"]
    ebs_base_url = ebs_consumer.objects.first().END_POINT
    verify_ssl =ebs_consumer.objects.first().VERIFY_SSL
    timeout = ebs_consumer.objects.first().TIMEOUT
    application_id = ebs_consumer.objects.first().APPLICATION_ID
   
    def get_payload_from_input(self, input_data):
        payload = {}
        payload.update(input_data)
        payload.update({'applicationId': self.application_id})
        payload.update({'UUID':str(uuid.uuid4())})
        return payload

    def get_response_data(self, ebs_response_content_json):
        ebs_response_content_json.pop('applicationId')
        return ebs_response_content_json
    
