from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
# Create your models here.
class CompleteCardRegistration(models.Model):
    
    applicationId         = models.CharField(max_length=100)
    tranDateTime          = models.DateTimeField()  # DDMMYYhhmmss / string(12) in EBS docs
    UUID                  = models.CharField(max_length=36, verbose_name='UUID')  # 
    originalTranUUID      = models.CharField(max_length=36, verbose_name='originalTranUUID')
    otp                   = models.CharField(_(""), max_length=50)
    IPIN                  = models.CharField(max_length=250,null=True)
    
class Register(models.Model):
    """
    This is for an abstract base class for the shared fields in Consumer Transaction reports.
    """
    applicationId         = models.CharField(max_length=100)
    tranDateTime          = models.DateTimeField()  # DDMMYYhhmmss / string(12) in EBS docs
    UUID                  = models.CharField(max_length=36, verbose_name='UUID')  # Universally Unique Identifier. This field should be sent with every request and is unique per request.
    expDate               = models.CharField(max_length=5,null=True)
    IPIN                  = models.CharField(max_length=250,null=True) 
    PAN                   = models.CharField(max_length=19,null=True)  # payer card number / PAN
    mbr = models.CharField(max_length=3,null=True)
    responseMessage = models.CharField(max_length=100,null=True)  # message to describe the response code
    responseCode = models.PositiveSmallIntegerField(null=True)  # 3 digit response code
    responseStatus = models.CharField(max_length=100,null=True)  # Transaction response status, either successful or failed
    request_date = models.DateTimeField(auto_now_add=True)  # our timestamp
    transaction_id = models.CharField(max_length=40,null=True)  # our ID for transaction
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
    PANCATEGORYCHOICE=(('Standard',_('Standard')),
                       ('Silver',_('Silver')),
                       ('Golden',_('Golden')),
                       ('Silver Agent',_('Silver Agent')),
                       ('Golden Agent',_('Golden Agent')))
    panCategory =models.CharField(max_length=12,default='Standard',choices=PANCATEGORYCHOICE,null=True)
    financialInstitutionId =models.CharField(max_length=4)
    
    fullName= models.CharField(max_length=255)
    dateOfBirth = models.DateField()
    CUSTOMERT_TYPE_CHOICE=(('National ID',_('National ID')),
                       ('Passport',_('Passport')),
                       ('Driving License',_('Driving License')),
    )
    customerIdType =models.CharField(max_length=36,default='National ID',choices=CUSTOMERT_TYPE_CHOICE,null=True)
    customerIdNumber =models.CharField(max_length=40)
    bankAccountNumber =models.CharField(max_length=36)
    ACCOUNT_TYPE_CHOICE=(
        ('Checking',_('Checking')),
        ('Savings',_('Savings')),
        ('Credit',_('Credit')),
        ('Bonus',_('Bonus')),
    )
    bankAccountType=models.CharField(max_length=36,default='Checking',choices=ACCOUNT_TYPE_CHOICE,null=True)
    bankBranchId= models.CharField(max_length=3)
    bankId =models.CharField(max_length=3)
    job  = models.CharField(max_length=50,null=True)
    email =models.EmailField(_('email address'), db_index=True, blank=True, null=True)
 