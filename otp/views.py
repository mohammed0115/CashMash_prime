import requests

from rest_framework.views import APIView
from rest_framework import generics, serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from accounts.models import User
from django.utils import timezone
import datetime
from django.contrib.auth import authenticate
from .otp_generation import GenerateOTP
# from apps.api_utilities.sms_gateway import SMSGateway, SERVICE_ID
from .sms import sms

import pyotp
from .serializers import OTPSerializer, OTPResetPasswordSerializer,VerificationOtpSerializer,changePasswordSerializer
from .models import OTP

from Consumer.permissions import HasValidAPIKey as ConsumerAPIKey
# from .permissions import HasValidAPIKey, IsCardHolderUser

class GenerateOTPView(generics.GenericAPIView):
    """The view that is reponsible for updating/creating otp"""

    serializer_class = OTPSerializer
    permission_classes = ()
    def checkUserIsFound(self,phone):
        if User.objects.filter(card_holder_mobile_number=phone).exists():
            return True
        else:
            return False
        
    def post(self, request, *args, **kwargs):
        required='card_holder_mobile_number'
        if required not in request.data:
            return Response({
                "responseStatus":"Failed","responseCode":350,"responseMessage":"the field [  "+required+" ]is required field."
                })
        if not self.checkUserIsFound(request.data[required]):
            return Response({"responseStatus":"Failed","responseCode":350,"responseMessage":"User is not exist please register first."})
        else:
            try:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                    # send the otp to our user
                message_body, private_key = self._prepare_message(
                        data=serializer.validated_data
                    )
                print(serializer.validated_data)
                altered_serialized_data = serializer.validated_data
                altered_serialized_data["private_key"] = private_key
                mobile_number = serializer.validated_data.get("card_holder_mobile_number")
                self._custom_update_or_create(altered_serialized_data, OTP)
                
                messageId = sms(message_body['MSG'],mobile_number)
                return Response(
                    {"sms_gateway": messageId.status_code,
                    "responseStatus":"Successful","responseCode":0,"responseMessage":"Approval"
                    }, status=status.HTTP_201_CREATED
                    )
            except Exception as e:
                return Response({"sms_gateway": "SMS Service is down. Consult our Provider",
                                    "responseStatus":"Failed","responseCode":205,"responseMessage":"ConnectionError"},
                            status=status.HTTP_504_GATEWAY_TIMEOUT
                            )        
    def _custom_update_or_create(self, data, model):
        mobile_number = data.get("card_holder_mobile_number")
        private_key = data.get("private_key")
        try:
            obj = model.objects.get(card_holder_mobile_number=mobile_number)
            obj.private_key = private_key
            obj.created_at = datetime.datetime.now()
            obj.save()
        except model.DoesNotExist:
            obj = model(
                card_holder_mobile_number=mobile_number, private_key=private_key
            )
            obj.save()

    def get_otp(self):
        return GenerateOTP.generate_otp()

    def _prepare_message(self, data):
        otp, secret_key = self.get_otp()
        print(otp)
        mobile_number = data.get("card_holder_mobile_number")
        welcome_message = "Your OTP is {}".format(otp)
        payload = {"mobileNo": mobile_number, "sourceType": 1, "MSG": welcome_message}
        return payload, secret_key





class VerifyOtpViews(generics.GenericAPIView):
    serializer_class = VerificationOtpSerializer
    permission_classes = ()
    def post(self,request, *args, **kwargs):
        # if verify_otp:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        verify_otp = self.verify_otp(data=serializer.validated_data)
        print(serializer.validated_data)
        mobile_number = serializer.data.get("card_holder_mobile_number")

        if verify_otp:
            
            return Response(
                {"message": "Otp verified","responseStatus":"Successful","responseCode":0,"responseMessage":"Approval"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                { "responseStatus":"Failed","responseCode":105,"responseMessage":"Invalid OTP"
                    ,
                    "detail": [
                        {
                            "error_message": "OTP is expired. Try a new one.",
                            "error_code": "otp_timed_out",
                        }
                    ]
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
    def verify_otp(self, data):
        mobile_number = data.get("card_holder_mobile_number")
        try:
            user = OTP.objects.get(card_holder_mobile_number=mobile_number)
            otp_time = user.created_at
            otp_private_key = user.private_key
            generated_otp, token = GenerateOTP.generate_otp(key=otp_private_key, for_time=20)
            print(generated_otp)
            delta_time = timezone.now() - otp_time
            mins = delta_time.total_seconds() / 60  # convert total seconds into mins
            print(mins)
            return GenerateOTP.verify_otp(data['otp'], otp_private_key, delta_time=int(mins))
        except OTP.DoesNotExist:
            return False
    
class ResetPassword(generics.GenericAPIView):
    serializer_class = OTPResetPasswordSerializer
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # verify_otp = self.verify_otp(data=serializer.validated_data)
            print(serializer.validated_data)
            mobile_number = serializer.data.get("card_holder_mobile_number")
            user = User.objects.get(card_holder_mobile_number=mobile_number)
            user.set_password(serializer.validated_data.get("password1"))
            user.save()
            return Response(
                {"message": "Password was reset","responseStatus":"Successful","responseCode":0,"responseMessage":"Approval"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                { "responseStatus":"Failed","responseCode":355,"responseMessage":serializer.errors
                   })
                
        # if verify_otp:
        #     # FIXME django issue #2070 or something about password retrieval time
        #     # and creating fake users to mitigate that.
        #     user = User.objects.get(card_holder_mobile_number=mobile_number)
        #     user.set_password(serializer.validated_data.get("password1"))
        #     user.save()
        #     return Response(
        #         {"message": "Password was reset","responseStatus":"Successful","responseCode":0,"responseMessage":"Approval"}, status=status.HTTP_200_OK
        #     )
        # else:
        #     return Response(
        #         { "responseStatus":"Failed","responseCode":105,"responseMessage":"Invalid OTP"
        #             ,
        #             "detail": [
        #                 {
        #                     "error_message": "OTP is expired. Try a new one.",
        #                     "error_code": "otp_timed_out",
        #                 }
        #             ]
        #         },
        #         status=status.HTTP_401_UNAUTHORIZED,
        #     )

    def verify_otp(self, data):

        mobile_number = data.get("card_holder_mobile_number")
        try:
            user = OTP.objects.get(card_holder_mobile_number=mobile_number)
            otp_time = user.created_at
            otp_private_key = user.private_key
            generated_otp, token = GenerateOTP.generate_otp(key=otp_private_key, for_time=20)
            print(generated_otp)
            delta_time = timezone.now() - otp_time
            mins = delta_time.total_seconds() / 60  # convert total seconds into mins
            print(mins)
            return GenerateOTP.verify_otp(generated_otp, otp_private_key, delta_time=int(mins))
        except OTP.DoesNotExist:
            return False






class RegisterOTpView(GenerateOTPView):
    def post(self, request, *args, **kwargs):
        required='card_holder_mobile_number'
        if required not in request.data:
            return Response({
                "responseStatus":"Failed","responseCode":350,"responseMessage":"the field [  "+required+" ]is required field."
                })
        if self.checkUserIsFound(request.data[required]):
            return Response({"responseStatus":"Failed","responseCode":350,"responseMessage":"User is already exist, please login."})
        else:
            try:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                    # send the otp to our user
                message_body, private_key = self._prepare_message(
                        data=serializer.validated_data
                    )
                print(serializer.validated_data)
                altered_serialized_data = serializer.validated_data
                altered_serialized_data["private_key"] = private_key
                mobile_number = serializer.validated_data.get("card_holder_mobile_number")
                self._custom_update_or_create(altered_serialized_data, OTP)
                
                messageId = sms(message_body['MSG'],mobile_number)
                return Response(
                    {"sms_gateway": messageId.status_code,
                    "responseStatus":"Successful","responseCode":0,"responseMessage":"Approval"
                    }, status=status.HTTP_201_CREATED
                    )
            except Exception as e:
                return Response({"sms_gateway": "SMS Service is down. Consult our Provider",
                                    "responseStatus":"Failed","responseCode":205,"responseMessage":"ConnectionError"},
                            status=status.HTTP_504_GATEWAY_TIMEOUT
                            )
class ChangePassword(generics.GenericAPIView):
    serializer_class = changePasswordSerializer
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # verify_otp = self.verify_otp(data=serializer.validated_data)
            print(serializer.validated_data)
            user = authenticate(card_holder_mobile_number=serializer.validated_data.get("card_holder_mobile_number"), password=serializer.validated_data.get("password"))
            if user:
                mobile_number = serializer.data.get("card_holder_mobile_number")
                user = User.objects.get(card_holder_mobile_number=mobile_number)
                user.set_password(serializer.validated_data.get("password1"))
                user.save()
                return Response(
                    {"message": "Password was changed","responseStatus":"Successful","responseCode":0,"responseMessage":"Approval"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    { "responseStatus":"Failed","responseCode":355,"responseMessage":"Invalid old passpword"
                    })
        else:
            return Response(
                { "responseStatus":"Failed","responseCode":355,"responseMessage":serializer.errors
                   })
            