import pytz
from datetime import date
from decimal import Decimal
from rest_framework import serializers
from django.utils.timezone import localtime, now
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.conf import settings

# import phonenumbers
class PanValidator(RegexValidator):
    code = 'invalid'

    def __init__(self):
        super(PanValidator, self).__init__(r"^([0-9]{16}|[0-9]{19})$",
                                           _('PAN should have either 16 or 19 digits.'))
class phoneValidator(RegexValidator):
    code = 'invalid'

    def __init__(self):
        super(PanValidator, self).__init__(r"^(249[0-9]{9})$",
                                           _('phone number should have either 10 or 13 digits.'))
class VoucherNumberValidator(RegexValidator):
    code = 'invalid'

    def __init__(self):
        super(VoucherNumberValidator, self).__init__(
            r"^[0-9]{10,20}$",
            _('Voucher Number should have at least 10 but not more than 20 digits.'))

class BaseConsumerAPISerializer(serializers.Serializer):
    tranDateTime = serializers.CharField(max_length=12)
    # applicationId = 
    # the regex is for accepting a uuid version 1 or version 4, checks case ignorant hex chars and groupings
    UUID = serializers.RegexField('^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}',max_length=36, min_length=36, allow_blank=False)
    class Meta:
          fields =['UUID','tranDateTime']
class userPasswordserializer(serializers.Serializer):
    userPassword    = serializers.CharField(max_length=250,required=False,allow_null=False)
class otpserializer(serializers.Serializer):
    otp  =serializers.CharField(max_length=6, allow_null=False)
class IPINerializer(serializers.Serializer):
    ipin = serializers.CharField(max_length=88, min_length=88, allow_null=False)


class authenticationSerializer(serializers.Serializer):
    authenticationType = serializers.ChoiceField(choices=['00','11' ], required=False,allow_null=False)  # defaults to '00'
class  PANserializer(serializers.Serializer):
    pan = serializers.CharField(allow_null=False, validators=[PanValidator()])
class PanExpDateserializer(serializers.Serializer):
    expDate = serializers.DateField(format='%y%m', input_formats=['%y%m'], allow_null=True)
    def validate_expDate(self, exp_date):
        """ Check card has not expired. """

        # make sure day is the same for comparison as it shouldn't matter, only care about month and year
        _expDate = exp_date.replace(day=1)
        today = localtime(now()).date().replace(day=1)
        if today > _expDate:  # same month is fine
            raise serializers.ValidationError("Card has expired.", code='expired')
        return exp_date
class mbrSerializer(serializers.Serializer):
    mbr = serializers.CharField(max_length=3, min_length=1, required=False,allow_null=True)    
class phoneNumberserializer(serializers.Serializer):
    phoneNumber   = serializers.CharField(allow_null=False, max_length=12)
class BasicUserAPISerializer(serializers.Serializer):
    userName        = serializers.CharField(max_length=250,required=False,allow_null=True)
    userPassword    = serializers.CharField(max_length=250,required=False,allow_null=True)
class doGenerateIPinRequestSerializer(BaseConsumerAPISerializer,
                                      BasicUserAPISerializer,
                                      PANserializer,
                                      phoneNumberserializer,
                                      PanExpDateserializer
                                      ):
    pass
class doGenerateCompletionIPinRequestSerializer(doGenerateIPinRequestSerializer,
                                                IPINerializer,
                                                otpserializer):
    pass