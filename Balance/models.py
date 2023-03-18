from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
class CommonTransaction(models.Model):
    tranDateTime =models.CharField("tranDateTime", max_length=50)
    UUID =models.CharField(max_length=36, verbose_name='UUID',unique=True)  # Universally Unique Identifier. This field should be sent with every request and is unique per request.
    phoneNo = models.CharField(max_length=12,null=True)  # store the current mobile number for the cardholder
    username = models.CharField(max_length=30,null=True)
    userPassword=models.CharField(max_length=30,null=True)
    Phone_No = "Phone No"
    Meter_No="Meter No"
    Credit_Card ="Credit Card"
    Cash_Card="Cash Card"
    Mobile_Wallet="Mobile Wallet"
    
    ENTITY_TYPE_CHOICES = (
        (Phone_No, _('Phone NO')),
        (Meter_No, _('Meter No')),
        (Credit_Card, _('Credit Card')),
        (Cash_Card, _('Credit Card')),
        (Mobile_Wallet, _(Mobile_Wallet)),
        )
    entityType  = models.CharField(_('entityID type'),default=Phone_No,choices=ENTITY_TYPE_CHOICES,max_length=20)
    entityId    = models.CharField(max_length=30,null=True)
    entityGroup = models.CharField(max_length=1,null=True)
    mbr = models.CharField(max_length=3,null=True)
    fromAccountType = models.CharField(max_length=2,null=True)  # from EBS
    fromAccount = models.CharField(max_length=30, null=True)
    responseMessage = models.CharField(max_length=100,null=True)  # message to describe the response code
    responseCode = models.PositiveSmallIntegerField(null=True)  # 3 digit response code
    responseStatus = models.CharField(max_length=100,null=True)  # Transaction response status, either successful or failed
    accountCurrency = models.CharField(max_length=3, null=True)
    balance = models.CharField(max_length=200, null=True)
    acqTranFee = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    issuer_fee = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    request_date = models.DateTimeField(auto_now_add=True,null=True)  # our timestamp
    transaction_id = models.CharField(max_length=40,null=True)  # our ID for transaction
    tranCurrency          = models.CharField(max_length=3,null=True)  # 3 letter currency code, EBS defaults to 'SDG'
    tranAmount            = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    expDate               = models.CharField(max_length=5,null=True)
    IPIN                  = models.CharField(max_length=250,null=True) 
    PAN                   = models.CharField(max_length=19,null=True)  # payer card number / PAN

class BalanceInquiry(CommonTransaction):
    pass
