import pytz
from datetime import date
from decimal import Decimal
from rest_framework import serializers
from django.utils.timezone import localtime, now
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.conf import settings
# from .models import TopUpCardTransaction

class PanValidator(RegexValidator):
    code = 'invalid'

    def __init__(self):
        super(PanValidator, self).__init__(r"^([0-9]{16}|[0-9]{19})$",
                                           _('PAN should have either 16 or 19 digits.'))
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

class authenticationSerializer(serializers.Serializer):
    authenticationType = serializers.ChoiceField(choices=['00','11' ], required=False,allow_null=False)  # defaults to '00'

class CardRequiredConsumerAPISerializer(BaseConsumerAPISerializer):
    PAN = serializers.CharField(allow_null=False, validators=[PanValidator()])
    IPIN = serializers.CharField(max_length=88, required=False,allow_null=True)
    expDate = serializers.DateField(format='%y%m', input_formats=['%y%m'], allow_null=True)
    mbr = serializers.CharField(max_length=3, min_length=1, required=False,allow_null=True)
    # we only allow PAN/iPIN authentication for now (option "00"). If this changes,
    # add more options from Appendix E in the EBS Consumer API docs
    


    def validate_expDate(self, exp_date):
        """ Check card has not expired. """

        # make sure day is the same for comparison as it shouldn't matter, only care about month and year
        _expDate = exp_date.replace(day=1)
        today = localtime(now()).date().replace(day=1)
        if today > _expDate:  # same month is fine
            raise serializers.ValidationError("Card has expired.", code='expired')
        return exp_date


class FromAccountConsumerAPISerializer(serializers.Serializer):
    # the from account type options are from Appendix G in the EBS Consumer API docs
    fromAccountType = serializers.ChoiceField(choices=['00', '01', '11', '31', '91'], required=False,allow_null=False)  # defaults to 00
    tranCurrency = serializers.ChoiceField(choices=['SDG', 'QAR', 'SAR', 'AED', 'USD', 'EUR'],
                                           required=False,allow_null=False)  # defaults to SDG

class toAccountConsumerAPISerializer(serializers.Serializer):
    # the from account type options are from Appendix G in the EBS Consumer API docs
    toAccountType = serializers.ChoiceField(choices=['00', '01', '11', '31', '91'], required=False,allow_null=False)  # defaults to 00
    
class PositiveAmountSerializer(serializers.Serializer):
    tranAmount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0.01'),
                                          allow_null=False)  # max is total number of digits including decimal


class PaymentInfoConsumerAPISerializer(serializers.Serializer):
    # Careful if changing, other serializer inherit fields
    payeeId = serializers.RegexField('^[0-9]*$', max_length=10, min_length=10, allow_blank=False)
    paymentInfo = serializers.CharField(min_length=1, max_length=999, allow_blank=False)











class TransactionStatusConsumerAPISerializer(BaseConsumerAPISerializer):
    originalTranUUID = serializers.RegexField(
        '^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}',
        max_length=36, min_length=36, allow_blank=False)
    


class CompleteTransactionSerializer(TransactionStatusConsumerAPISerializer):
    OTP     = serializers.CharField(max_length=6, allow_null=False)




    
    
    
    
class CardTransferAPISerializer(CardRequiredConsumerAPISerializer, FromAccountConsumerAPISerializer,
                                PositiveAmountSerializer):
    toCard = serializers.CharField(allow_null=False, validators=[PanValidator()])
    toAccountType = serializers.ChoiceField(choices=['00', '01', '11', '31', '91'], required=False,allow_null=False)  # defaults to 00

class CardHolderTopUpTransactionRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        # model = TopUpCardTransaction
        # Terminal ID and EBS approval codes and references are not returned as they aren't useful for a card holder
        fields = ('transaction_id', 'tranDateTime', 'last_4_digits_of_pan',
                  'tranAmount', 'tranCurrency', 'response_message',
                  'response_status', 'transaction_fee', 'additional_amount')

class CardBalanceInquirySerializer(CardRequiredConsumerAPISerializer, FromAccountConsumerAPISerializer):
    # no extra fields, just the combined CardRequiredConsumerAPISerializer and FromAccountConsumerAPISerializer fields
    pass


 
    

class EntitySerializer(serializers.Serializer):
    entityId        = serializers.CharField(max_length=100,required=False,allow_null=False)
    entityType      = serializers.CharField(max_length=20,required=False,allow_null=False)
    # def validate_entityType(self, entityType):
    #     """ Check card has not expired. """
    #     entitylitst=['Phone No','Meter No','Credit Card','Cash Card','Mobile Wallet']
    #     if entityType not in entitylitst:
    #         raise serializers.ValidationError(entitylitst, code='invalid')
class BasicUserAPISerializer(serializers.Serializer):
    userName        = serializers.CharField(max_length=250,required=False,allow_null=True)
    userPassword    = serializers.CharField(max_length=250,required=False,allow_null=True)
    
class paymentDetailsSerializer(serializers.Serializer):
    accounts        = serializers.CharField(max_length=250,required=False,allow_null=False)
    descriptions    = serializers.CharField(max_length=250,required=False,allow_null=False)
    amounts        = serializers.CharField(max_length=100,required=False,allow_null=False)
class extraInforSerializer(serializers.Serializer):
    securityQuestion= serializers.CharField(max_length=100,required=False,allow_null=False)
    securityQuestionAnswer =serializers.CharField(max_length=17,min_length=4,required=False,allow_null=False)

class BankSerializer(serializers.Serializer):
    bankAccountType       =serializers.CharField(max_length=12,required=False,allow_null=False)
    bankBranchId          =serializers.CharField(max_length=3,required=False,allow_null=False)
    bankId                =serializers.CharField(max_length=4,required=False,allow_null=False)
class CustomerSerializer(serializers.Serializer):
    customerIdNumber      = serializers.CharField(max_length=40,required=False,allow_null=False)
    customerIdType        =serializers.CharField(max_length=36,required=False,allow_null=False)
class userPasswordserializer(serializers.Serializer):
    userPassword    = serializers.CharField(max_length=250,required=False,allow_null=False)

    
class QRPurchaseSerializer(BaseConsumerAPISerializer,
                               EntitySerializer,
                               userPasswordserializer):
    authenticationType = serializers.ChoiceField(choices=['00', '11'], required=False,allow_null=False)

class ChangePasswordSerializer(BaseConsumerAPISerializer,
                               EntitySerializer,
                               userPasswordserializer):
    IPIN = serializers.CharField(max_length=88, min_length=88, allow_null=False)
    authenticationType = serializers.ChoiceField(choices=['00', "11"], required=False,allow_null=False)
    newUserPassword    = serializers.CharField(max_length=250,required=False,allow_null=False)
class ForgetPasswordSerializer(BaseConsumerAPISerializer,
                               EntitySerializer,
                               userPasswordserializer):
    # IPIN = serializers.CharField(max_length=88, min_length=88, allow_null=False)
    authenticationType = serializers.ChoiceField(choices=['00','11' ], required=False,allow_null=False)
    newUserPassword    = serializers.CharField(max_length=250,required=False,allow_null=False)
    securityQuestion= serializers.CharField(max_length=100,required=False,allow_null=False)
    securityQuestionAnswer =serializers.CharField(max_length=17,min_length=4,required=False,allow_null=False)

    
    


 

class BalanceInqueryAPISerializer(EntitySerializer,
                                  authenticationSerializer,
                                  BasicUserAPISerializer,
                                  FromAccountConsumerAPISerializer,
                                  BaseConsumerAPISerializer
                                  ):
    PAN = serializers.CharField(allow_null=False, validators=[PanValidator()])
    # IPIN = serializers.CharField(max_length=88, required=False,allow_null=True)
    expDate = serializers.DateField(format='%y%m', input_formats=['%y%m'], allow_null=True)
    mbr = serializers.CharField(max_length=3, min_length=1, required=False,allow_null=True)
class BillInquiryConsumerAPISerializer(
                                       
                                       BaseConsumerAPISerializer,
                                       EntitySerializer,
                                       authenticationSerializer,
                                    #    BasicUserAPISerializer, 
                                       PaymentInfoConsumerAPISerializer
                                       ):
    
    """
        tranDateTime
        UUID
        userPassword
        entityId
        entityType
        # PAN
        # expDate
        # mbr
        payeeId
        paymentInfo
        authenticationType
    
    """
    # no extra fields, just the combined CardRequiredConsumerAPISerializer and PaymentInfoConsumerAPISerializer fields
    # PAN = serializers.CharField(allow_null=False, validators=[PanValidator()])
    # IPIN = serializers.CharField(max_length=88, required=False,allow_null=True)
    # expDate = serializers.DateField(format='%y%m', input_formats=['%y%m'], allow_null=True)
    mbr = serializers.CharField(max_length=3, min_length=1, required=False,allow_null=True)
    userPassword    = serializers.CharField(max_length=250,required=False,allow_null=True)
class BillInquiryConsumerAPISerializerPan(
                                       
                                       BaseConsumerAPISerializer,
                                       authenticationSerializer,
                                       PaymentInfoConsumerAPISerializer
                                       ):
    
    """
        tranDateTime
        UUID
        userPassword
        entityId
        entityType
        # PAN
        # expDate
        # mbr
        payeeId
        paymentInfo
        authenticationType
    
    """
    # no extra fields, just the combined CardRequiredConsumerAPISerializer and PaymentInfoConsumerAPISerializer fields
    PAN = serializers.CharField(allow_null=False, validators=[PanValidator()])
    IPIN = serializers.CharField(max_length=88, required=False,allow_null=True)
    expDate = serializers.DateField(format='%y%m', input_formats=['%y%m'], allow_null=True)
    mbr = serializers.CharField(max_length=3, min_length=1, required=False,allow_null=True)  

class PaymentConsumerAPISerializerEntity(BillInquiryConsumerAPISerializer, 
                                   FromAccountConsumerAPISerializer,
                                     PositiveAmountSerializer):
    # no extra fields
    pass
class CompletecardregistrationSerializer(BaseConsumerAPISerializer,userPasswordserializer):
    IPIN    = serializers.CharField(max_length=88, min_length=88, allow_null=False)
    otp     = serializers.CharField(max_length=6, allow_null=False)
    extraInfo    = extraInforSerializer()
    originalTranUUID = serializers.RegexField(
        '^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}',
        max_length=36, min_length=36, allow_blank=False)


class ServicePaymentConsumerAPISerializer(CardRequiredConsumerAPISerializer, FromAccountConsumerAPISerializer,
                                          PositiveAmountSerializer):
    serviceProviderId = serializers.CharField(allow_null=False, min_length=10, max_length=10, required=True)
    # serviceInfo = serializers.CharField(allow_null=True, min_length=1, max_length=100, required=False,allow_null=False)
class CardTransferAPISerializer( 
                                 BaseConsumerAPISerializer,
                                 authenticationSerializer,
                                 EntitySerializer,
                                 FromAccountConsumerAPISerializer,
                                 PositiveAmountSerializer):
    mbr = serializers.CharField(max_length=3, min_length=1, required=False,allow_null=True)
    userPassword    = serializers.CharField(max_length=250,required=False,allow_null=True)
    toCard = serializers.CharField(allow_null=False, validators=[PanValidator()])
    toAccountType = serializers.ChoiceField(choices=['00', '01', '11', '31', '91'], required=False,allow_null=False)  # defaults to 00
class GenerateVoucherConsumerAPISerializer(BaseConsumerAPISerializer,
                                           authenticationSerializer,
                                           EntitySerializer,
                                            FromAccountConsumerAPISerializer):
    voucherNumber = serializers.CharField(validators=[VoucherNumberValidator()])
    tranAmount = serializers.DecimalField(allow_null=False, max_digits=12, decimal_places=2, min_value=10)

    def validate_tranAmount(self, tranAmount):
        """
        Check that the tranAmount is a multiple of ten.
        The vouchers are usually cashed from ATMs so the amount needs to be suitable for that.
        """
        if tranAmount % 10 != 0:
            raise serializers.ValidationError("Amount should be multiple of 10.", code='invalid_amount')

        return tranAmount
class ChangeCardsIpin(BaseConsumerAPISerializer,
                                 authenticationSerializer,
                                 EntitySerializer):
    newIPIN = serializers.CharField(max_length=88, min_length=88, allow_null=False)
    userPassword    = serializers.CharField(max_length=250,required=False,allow_null=True)
    
class QRRefundSerializer(BasicUserAPISerializer,CompletecardregistrationSerializer):
    authenticationType = serializers.ChoiceField(choices=['00', ], required=False,allow_null=False)