from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from Consumer.models import PaymentTransaction, GenerateVoucherTransaction, ServicePaymentTransaction, \
    CardTransferTransaction,TopUpCardTransaction,PurchaseTransaction,BillPaymentTransaction

morsal_fields = ['request_date', 'transaction_id', 'user_id', 'user_mobile_number']

transaction_fields = ['UUID', 'tranCurrency', 'tranAmount', 'tranDateTime','PAN', 'mbr']

response_fields = ['fromAccountType', 'fromAccount', 'acqTranFee', 'issuer_fee', 'accountCurrency', 'balance',
                   'responseMessage', 'responseCode', 'responseStatus', ]

common_fields =  transaction_fields + response_fields
# class RegisterAdmin(MaskedPanMixin, admin.ModelAdmin):
#     custom_fields = ['payee_id', 'payment_info', 'bill_info']
#     readonly_fields = common_fields + custom_fields
#     search_fields = ['transaction_id', 'UUID']
#     list_display = common_fields + custom_fields
#     fieldsets = (
#         ('Morsal Information', {
#             'fields': morsal_fields
#         }),
#         ('Transaction Information', {
#             'fields': transaction_fields + ['payee_id', 'payment_info',]
#         }),
#         ('EBS Response', {
#             'fields': response_fields + ['bill_info',]
#         }),
#     )
