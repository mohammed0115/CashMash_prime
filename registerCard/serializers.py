import pytz
from datetime import date
from decimal import Decimal
from rest_framework import serializers
from django.utils.timezone import localtime, now
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.conf import settings
from Consumer.serializers import BaseConsumerAPISerializer,CardRequiredConsumerAPISerializer,PanValidator
from .models import *


class registrationTypeValidator(RegexValidator):
    code = 'invalid'

    def __init__(self):
        super(registrationTypeValidator, self).__init__(r"^([01]|[10]|[12]|[00])$",
                                           _("registrationType should be in ['01','10','12' or '00']"))
        
        
class userPasswordserializer(serializers.Serializer):
    userPassword    = serializers.CharField(max_length=250)
    
class CompletecardregistrationSerializer(BaseConsumerAPISerializer,userPasswordserializer):
    IPIN = serializers.CharField(max_length=88, min_length=88, allow_null=False)
    otp  =serializers.CharField(max_length=6, allow_null=False)

class CustomerSerializer(serializers.Serializer):
    customerIdNumber      = serializers.CharField(max_length=40)
    customerIdType        =serializers.CharField(max_length=36)
class EntityUserAPISerializer(serializers.Serializer):
    # userName        = serializers.CharField(max_length=250,required=False,allow_null=False)
    # userPassword    = serializers.CharField(max_length=250,required=False,allow_null=False)
    entityId        = serializers.CharField(max_length=40,)
    entityType      = serializers.CharField(max_length=20)
    entityGroup           = serializers.CharField(max_length=2,required=False,allow_null=False)
    
    # def validate_entityType(self, entityType):
    #     """ Check card has not expired. """
    #     entitylitst=['Phone No','Meter No','Credit Card','Cash Card','Mobile Wallet']
    #     if entityType not in entitylitst:
    #         raise serializers.ValidationError(entitylitst, code='invalid')
class UserNameSerializer(serializers.Serializer):
    userName        = serializers.CharField(max_length=250,required=False,allow_null=False)
class extraInforSerializer(serializers.Serializer):
    securityQuestion= serializers.CharField(max_length=100,required=False,allow_null=False)
    securityQuestionAnswer =serializers.CharField(max_length=17,min_length=4,required=False,allow_null=False)
class PanSerializer(serializers.Serializer):
    PAN = serializers.CharField(allow_null=False, validators=[PanValidator()])
class CardRequiredInfoAPISerializer(serializers.Serializer):
    IPIN = serializers.CharField(max_length=88, allow_null=False)
    expDate = serializers.DateField(format='%y%m', input_formats=['%y%m'], allow_null=False)
    mbr = serializers.CharField(max_length=3, min_length=1, required=False,allow_null=False)
    # defaults to '00'


    def validate_expDate(self, exp_date):
        """ Check card has not expired. """

        # make sure day is the same for comparison as it shouldn't matter, only care about month and year
        _expDate = exp_date.replace(day=1)
        today = localtime(now()).date().replace(day=1)
        if today > _expDate:  # same month is fine
            raise serializers.ValidationError("Card has expired.", code='expired')
        return exp_date
    
class BankSerializer(serializers.Serializer):
    bankAccountNumber     =serializers.CharField(max_length=4,required=False,allow_null=False)
    bankAccountType       =serializers.CharField(max_length=12,required=False,allow_null=False)
    bankBranchId          =serializers.CharField(max_length=3,required=False,allow_null=False)
    bankId                =serializers.CharField(max_length=4,required=False,allow_null=False)



class RegisterSerializer(EntityUserAPISerializer,UserNameSerializer,
                         userPasswordserializer,BaseConsumerAPISerializer,BankSerializer,CustomerSerializer,CardRequiredInfoAPISerializer,PanSerializer):
    registrationType      = serializers.CharField(validators=[registrationTypeValidator],max_length=3,allow_null=False)
    fullName              = serializers.CharField(max_length=255,min_length=5,required=False,allow_null=False)
    financialInstitutionId=serializers.CharField(max_length=4,allow_null=False)
    panCategory           =serializers.CharField(max_length=10,allow_null=False)
    dateOfBirth           = serializers.DateField(allow_null=False,format="%d-%m-%Y")
    job                   =serializers.CharField(max_length=50,required=False,allow_null=False)
    email                 =serializers.EmailField(required=False,allow_null=False)
    extraInfo             =extraInforSerializer()
    
    

class phoneNoSerializers(serializers.Serializer):
    phoneNo = serializers.CharField(max_length=12,allow_null=True)
class GoldenCardSerializer(RegisterSerializer):
    model=Register
    fields="__all__"
class SilverCardSerializer(EntityUserAPISerializer,UserNameSerializer,
                         userPasswordserializer,BaseConsumerAPISerializer,CardRequiredInfoAPISerializer):
    registrationType      = serializers.CharField(validators=[registrationTypeValidator],max_length=2,allow_null=False)
    financialInstitutionId=serializers.CharField(max_length=4,allow_null=False)
    panCategory           =serializers.CharField(max_length=10,allow_null=False)
    job                   =serializers.CharField(max_length=50,required=False,allow_null=False)
    email                 =serializers.EmailField(required=False,allow_null=False)
    extraInfo             =extraInforSerializer()
    class Meta:
        model=Register
        fields=['tranDateTime','UUID','userName','entityId','entityType','entityGroup','phoneNo','registrationType','userPassword','financialInstitutionId','panCategory',
                'job','email','PAN','IPIN','expDate','mbr'
                ]
    
    
class VirtualCardSerializer(BaseConsumerAPISerializer,UserNameSerializer,EntityUserAPISerializer,phoneNoSerializers):
    class Meta:
        model=Register
        fields=['tranDateTime','UUID','userName','entityId','entityType','entityGroup','phoneNo','registrationType'
                ]
    