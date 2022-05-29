from django.shortcuts import render

# Create your views here.
from .models import Card 
from .serializers import Cardserializers
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from accounts.authentication import CardHolderAccessTokenAuthentication
from Consumer.permissions import HasValidAPIKey, IsCardHolderUser
from Consumer.auth.utils import get_access_token
from APIKEY.models import BlockedToken
from accounts.models import User as User
from Consumer.auth.views import ObtainJSONWebTokenAPIView, BaseRefreshUserTokenView
from rest_framework.authentication import get_authorization_header
class CardList(ObtainJSONWebTokenAPIView):
    authentication_classes = (CardHolderAccessTokenAuthentication,JSONWebTokenAuthentication)
    permission_classes = ()
    queryset = Card.objects.all()
    serializer_class = Cardserializers
    # def get(self, request, *args, **kwargs):
    #     # get_user_by_username
    #     print(request)
    #     self.queryset=Card.objects.filter(card_user=request.data.get('user_id'))
    #     serializer = self.serializer_class(self.queryset,many=True)
    #     return Response(self.success_response(serializer))
            
        
    def success_response(self,serializer):
        return {"cards":serializer.data,"responseStatus":"Successful","responseCode":0,"responseMessage":"Approval"}
    def failed_response(self,serializer):
        return {"errors":serializer.errors,"responseStatus":"Failed","responseCode":505,"responseMessage":serializer.errors}
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(self.success_response(serializer), status=status.HTTP_201_CREATED)
        return Response(self.failed_response, status=200)
            
class getCard(APIView):
    authentication_classes = (CardHolderAccessTokenAuthentication,JSONWebTokenAuthentication)
    permission_classes = ()
    queryset = Card.objects.all()
    serializer_class = Cardserializers
    def success_response(self,serializer):
        return {"cards":serializer.data,"responseStatus":"Successful","responseCode":0,"responseMessage":"Approval"}
    def failed_response(self,serializer):
        return {"errors":serializer.errors,"responseStatus":"Failed","responseCode":505,"responseMessage":serializer.errors}

    def get(self,request,id):
        # get_user_by_username
        # print(request)
        self.queryset=Card.objects.filter(card_user=id)
        serializer = self.serializer_class(self.queryset,many=True)
        return Response(self.success_response(serializer))     
class CardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = Cardserializers