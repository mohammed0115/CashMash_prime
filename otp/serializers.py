from django.utils.translation import ugettext as _

from django.contrib.auth import password_validation
from rest_framework import serializers
from .models import OTP
# from accounts.serializers import CardHolderUserLoginRequestSerializer
from accounts.validators import CustomPasswordValidator
from Consumer.auth.serializers import BaseObtainTokenSerializer
from Consumer.auth.authentication import validate_password


from accounts.validators import CardHolderMobileNumberValidator, CustomPasswordValidator
from Consumer.auth.authentication import validate_password
from Consumer.authentication import authenticate_card_holder_user

class OTPSerializer(serializers.ModelSerializer):
    """This class is used to serialize OTP model."""

    class Meta:
        model = OTP
        fields = "__all__"

class VerificationOtpSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    card_holder_mobile_number = serializers.CharField(max_length=10, required=True)
    
class OTPResetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(min_length=4)
    password2 = serializers.CharField(min_length=4)
    otp = serializers.CharField(max_length=6,allow_null=True,required=False)
    card_holder_mobile_number = serializers.CharField(max_length=10, required=True)

    def validate_password1(self, password):
        password_validators = [
            # CustomPasswordValidator(),
            password_validation.MinimumLengthValidator(min_length=4),
            # password_validation.CommonPasswordValidator(),
            # password_validation.NumericPasswordValidator(),
        ]
        validate_password(password, None, password_validators=password_validators)
        return password

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError(
                {"password2": _("The two password fields didn't match.")},
                code="passwords_not_match",
            )
            # TODO validate mobile_number too. it will be validated anyway
        return data
    
class changePasswordSerializer(BaseObtainTokenSerializer):
    password1 = serializers.CharField(min_length=4)
    password2 = serializers.CharField(min_length=4)
    user_model_username_field = 'card_holder_mobile_number'

    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super(BaseObtainTokenSerializer, self).__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(validators=[CardHolderMobileNumberValidator()])
    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError(
                {"password2": _("The two password fields didn't match.")},
                code="passwords_not_match",
            )
            # TODO validate mobile_number too. it will be validated anyway
        return data
    

    def authenticate(self, username, password):
        return authenticate_card_holder_user(username, password)
