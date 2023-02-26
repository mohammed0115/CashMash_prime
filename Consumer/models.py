from django.db import models

# Create your models here.
from datetime import datetime
from django.db import models
from accounts.models import User

class ConsumerBaseTransaction(models.Model):
    """
    This is for an abstract base class for the shared fields in Consumer Transaction reports.
    """
    applicationId         = models.CharField(max_length=100)
    tranDateTime          = models.DateTimeField()  # DDMMYYhhmmss / string(12) in EBS docs
    UUID                  = models.CharField(max_length=36, verbose_name='UUID')  # Universally Unique Identifier. This field should be sent with every request and is unique per request.
    tranCurrency          = models.CharField(max_length=3,null=True)  # 3 letter currency code, EBS defaults to 'SDG'
    tranAmount            = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    expDate               = models.CharField(max_length=5,null=True)
    IPIN                  = models.CharField(max_length=250,null=True) 
    PAN                   = models.CharField(max_length=19,null=True)  # payer card number / PAN
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
    user_id = models.IntegerField(null=True)  # store the user id as static
    user_mobile_number = models.CharField(max_length=20,null=True)  # store the current mobile number for the cardholder

    class Meta:
        abstract = True

    def masked_pan(self):
        if self.PAN and len(self.PAN) > 4:
            return len(self.PAN[:-4]) * '*' + self.PAN[-4:]
        else:
            return self.PAN

    def __str__(self):
        return self.transaction_id
    def last_4_digits_of_pan(self):
        if len(self.PAN) > 4:
            return self.PAN[-4:]
        return self.PAN



class PaymentTransaction(ConsumerBaseTransaction):
    """
    This is the report for MakePayment - EBS 3.6 Payment
    """

    payee_id = models.CharField(max_length=10)
    payment_info = models.CharField(max_length=999)
    bill_info = models.CharField(max_length=999, null=True)

    class Meta:
        verbose_name = 'Payment Transaction'
        verbose_name_plural = 'Payment Transaction Report'


class CardTransferTransaction(ConsumerBaseTransaction):
    """
    This is the report for card to card transfer - EBS 3.8 Card Transfer
    """

    to_card = models.CharField(max_length=19)
    to_account_type = models.CharField(max_length=2, null=True)
    to_account = models.CharField(max_length=30, null=True)

    class Meta:
        verbose_name = 'Card Transfer Transaction'
        verbose_name_plural = 'Card Transfer Transaction Report'


class GenerateVoucherTransaction(ConsumerBaseTransaction):
    """
    This is the report for Generating voucher - EBS 3.14 Generate voucher
    """

    voucher_number = models.CharField(max_length=20)
    voucher_code = models.CharField(max_length=10, null=True)

    class Meta:
        verbose_name = 'Generate Voucher Transaction'
        verbose_name_plural = 'Generate Voucher Transaction Report'


class ServicePaymentTransaction(ConsumerBaseTransaction):
    """
    This is the report for making a service payment- EBS 3.15 Service Payment
    """

    service_provider_id = models.CharField(max_length=10, null=True)
    service_info = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = 'Service Payment Transaction'
        verbose_name_plural = 'Service Payment Transaction Report'
class TopUpCardTransaction(ConsumerBaseTransaction):
    
    class Meta:
        verbose_name = 'Top-up Transaction'
        verbose_name_plural = 'Top-up Transactions'


class PurchaseTransaction(ConsumerBaseTransaction):

    class Meta:
        verbose_name = 'Purchase Transaction'
        verbose_name_plural = 'Purchase Transactions'
        
class BillPaymentTransaction(ConsumerBaseTransaction):
    personal_payment_info = models.CharField(max_length=30)
    payee_id = models.CharField(max_length=10)
    additional_data = models.TextField(null=True, blank=True)

    def payee_name(self):
        payees = {
            "0010010001": "Zain Top Up",
            "0010010003": "MTN Top up",
            "0010010005": "Sudani Top Up",
            "0010010002": "Zain Bill Payment",
            "0010010004": "MTN Bill Payment",
            "0010010006": "Sudani Bill Payment",
            "0010020001": "SEDC",
            "0010030002": "MOHE",
            "0010030003": "customs",
            "0010030004": "MOHE Arab",
            "0010030006": "e15",
            "0010050001": "E15",
        }
        return payees.get(self.payee_id, "")

# class register(ConsumerBaseTransaction):
#     pass
# class completeCardRegistration():
#     pass
class getBalance(ConsumerBaseTransaction):
    pass
# class getBill():
#     pass
# class isAlive():
#     pass
class getPayeesList(ConsumerBaseTransaction):
    pass
# class changePassword():
#     pass
# class changeIPin():
#     pass
# class adminResetPassword():
#     pass





class Card(models.Model):
    # perso_file = models.ForeignKey(PERSOFile, on_delete=models.SET_NULL, null=True)
    pan = models.CharField(max_length=19, db_index=True, verbose_name='PAN')
    expires_end = models.CharField(max_length=5)
    name = models.CharField(max_length=20, blank=True, null=True)
    # cvv = models.CharField(max_length=3, verbose_name='CVV')
    # iso1 = models.CharField(max_length=100, verbose_name='ISO1')
    # iso2 = models.CharField(max_length=100, verbose_name='ISO2')
    mbr = models.IntegerField(db_index=True, default=0,verbose_name='MBR')
    # batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)
    # suspended = models.BooleanField(default=False)
    # lost = models.BooleanField(default=False)
    card_holder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # financial_institution = models.ForeignKey(FinancialInstitution, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = (('pan', 'mbr'),)

    def __str__(self):
        return str(self.id)

    @property
    def last_4_digits_of_pan(self):
        return self.pan[-4:]

    CARD_STATUS_UNASSIGNED = 0
    CARD_STATUS_ASSIGNED = 1