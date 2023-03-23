import datetime
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from Consumer.auth.views import ObtainJSONWebTokenAPIView, BaseRefreshUserTokenView
from Consumer.auth.utils import get_access_token
# from rest_framework.authtoken.views import ObtainAuthToken
from accounts.authentication import CardHolderAccessTokenAuthentication
from Consumer.permissions import HasValidAPIKey, IsCardHolderUser
from APIKEY.models import BlockedToken
from .serializers import CardHolderUserLoginRequestSerializer, CardHolderUserRetrieveSerializer, \
    CardHolderUserCreationSerializer,CardHolderUserCreationSerializer1
from rest_framework import status
from accounts.models import User
from Consumer.auth.utils import generate_jwt_token_payload,encode_jwt_token_payload
from rest_framework.exceptions import APIException
from rest_framework_jwt import views as jwt_views




from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import requests



def generateOTP(phone):
    url = "http://45.77.252.45/accounts/RegisterOTp/"

    payload={
        "card_holder_mobile_number":phone,
            }
    headers = {
    'Content-Type': 'application/json'
    }

    return requests.request("POST", url, headers=headers, json=payload)

    


class LoginUserView(ObtainJSONWebTokenAPIView):
    serializer_class = CardHolderUserLoginRequestSerializer
    permission_classes = ()

    def get_response_payload(self, token, user=None, request=None):
        """
        Returns the response data for both the login and refresh views.
        Override to return a custom response such as including the
        serialized representation of the User.
        """
        return {
            'token': token,
            'user': CardHolderUserRetrieveSerializer(user, context={'request': request}).data,
            "responseStatus":"Successful","responseCode":0,"responseMessage":"Approval"
        }


class LogoutUserView(APIView):
    permission_classes = ()
    authentication_classes = (CardHolderAccessTokenAuthentication,)

    def post(self, request, *args, **kwargs):
        try:
            current_token = get_access_token(request)
            d,j=BlockedToken.objects.update_or_create(token=current_token)
            d.save()
            return Response({"responseStatus":"Successful","responseCode":0,"responseMessage":"Approval"})
        except APIException as e:
            status_code = 500
            return Response({
                             "responseStatus":"Failed","responseCode":status_code,"responseMessage":str(e)},
                    status=200
                    )

class RefreshUserTokenView(BaseRefreshUserTokenView):
    permission_classes = ()
    authentication_classes = ()
    username_field = 'card_holder_mobile_number'

    def post(self, request, *args, **kwargs):
        # add the old token to the blocked list
        old_token = get_access_token(request)
        d,j=BlockedToken.objects.update_or_create(token=old_token)
        d.save()
        return super(RefreshUserTokenView, self).post(request, *args, **kwargs)
class RegisterUserView1(CreateAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = CardHolderUserCreationSerializer

class RegisterUserView(ObtainJSONWebTokenAPIView):
    permission_classes = ()
    authentication_classes = ()
    username_field = 'card_holder_mobile_number'
    serializer_class = CardHolderUserCreationSerializer1
    def checkUserIsFound(self,phone):
        if User.objects.filter(card_holder_mobile_number=phone).exists():
            return True
        else:
            return False
    def post(self, request, *args, **kwargs):
        required=[
                        
                        "full_name",
                        "mobile_number",
                        "email",
                        "gender",
                        "date_of_birth",
                        "address",
                        "state",
                        "city",
                        "id_type",
                        "id_number",
                        "password",
                        "password2"
        ]
        for i in required:
            if i not in request.data:
                break
                return Response({"responseStatus":"Failed","responseCode":88,
                                 "responseMessage":"Sadad required failed error",
                                 "[ the field "+i+"]":"is required"},status=200)
        if self.checkUserIsFound(request.data.get('mobile_number')):
            return Response({"responseStatus":"Failed","responseCode":250,
                             "responseMessage":"User already exists."},status=200)
        try:
            serializer =  serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                user = User.objects.get(card_holder_mobile_number=request.data.get('mobile_number'))
                payload= generate_jwt_token_payload(user, self.username_field)
                token = encode_jwt_token_payload(payload)
                response_data = self.get_response_payload(token, user, request)
                otp=generateOTP(request.data.get('mobile_number'))
                # if otp.status_code==200:
                #     otp=otp.json()
                #     if otp['responseCode']==0:
                #         response_data.update({
                #             "sms_gateway":otp['sms_gateway']
                #         })
                # else:
                #     response_data.update({
                #             "sms_gateway":otp
                #         })
                        
                
                response = Response(response_data)
                # response = Response(token)
                return response
        except APIException as e:
            status_code = 503
            return Response({
                             "responseStatus":"Failed","responseCode":status_code,"responseMessage":str(e)},
                    status=200
                    )
    def get_response_payload(self, token,user=None, request=None):
        """
        Returns the response data for both the login and refresh views.
        Override to return a custom response such as including the
        serialized representation of the User.
        """
        return {
            'token': token,
            'user': CardHolderUserRetrieveSerializer(user, context={'request': request}).data,
            "responseStatus":"Successful","responseCode":0,"responseMessage":"Approval"
        }