from django.contrib import admin

# Register your models here.
from Consumer.models import PaymentTransaction, GenerateVoucherTransaction, ServicePaymentTransaction, \
    CardTransferTransaction,TopUpCardTransaction,PurchaseTransaction,BillPaymentTransaction

morsal_fields = ['request_date', 'transaction_id', 'user_id', 'user_mobile_number']

transaction_fields = ['UUID', 'tranCurrency', 'tranAmount', 'tranDateTime','PAN', 'mbr']

response_fields = ['fromAccountType', 'fromAccount', 'acqTranFee', 'issuer_fee', 'accountCurrency', 'balance',
                   'responseMessage', 'responseCode', 'responseStatus', ]

common_fields =  transaction_fields + response_fields


class MaskedPanMixin:

    def masked_pan(self, obj):
        return obj.masked_pan()

    masked_pan.short_description = 'PAN'


class PaymentTransactionAdmin(MaskedPanMixin, admin.ModelAdmin):
    custom_fields = ['payee_id', 'payment_info', 'bill_info']
    readonly_fields = common_fields + custom_fields
    search_fields = ['transaction_id', 'UUID']
    list_display = common_fields + custom_fields
    fieldsets = (
        ('Morsal Information', {
            'fields': morsal_fields
        }),
        ('Transaction Information', {
            'fields': transaction_fields + ['payee_id', 'payment_info',]
        }),
        ('EBS Response', {
            'fields': response_fields + ['bill_info',]
        }),
    )


class CardTransferTransactionAdmin(MaskedPanMixin, admin.ModelAdmin):
    custom_fields = ['to_card', 'to_account_type', 'to_account']
    readonly_fields = common_fields + custom_fields
    search_fields = ['transaction_id', 'UUID']
    list_display = common_fields + custom_fields
    fieldsets = (
        ('Morsal Information', {
            'fields': morsal_fields
        }),
        ('Transaction Information', {
            'fields': transaction_fields + ['to_card', 'to_account_type',]
        }),
        ('EBS Response', {
            'fields': response_fields + ['to_account',]
        }),
    )


class GenerateVoucherTransactionAdmin(MaskedPanMixin, admin.ModelAdmin):
    custom_fields = ['voucher_number', 'voucher_code']
    readonly_fields = common_fields + custom_fields
    search_fields = ['transaction_id', 'UUID']
    list_display = common_fields + custom_fields
    fieldsets = (
        ('Morsal Information', {
            'fields': morsal_fields
        }),
        ('Transaction Information', {
            'fields': transaction_fields + ['voucher_number',]
        }),
        ('EBS Response', {
            'fields': response_fields + ['voucher_code',]
        }),
    )


class ServicePaymentTransactionAdmin(MaskedPanMixin, admin.ModelAdmin):
    custom_fields = ['service_provider_id', 'service_info']
    readonly_fields = common_fields + custom_fields
    search_fields = ['transaction_id', 'UUID']
    list_display = common_fields + custom_fields
    fieldsets = (
        ('Morsal Information', {
            'fields': morsal_fields
        }),
        ('Transaction Information', {
            'fields': transaction_fields + ['service_provider_id', 'service_info']
        }),
        ('EBS Response', {
            'fields': response_fields
        }),
    )
class TopUpCardTransactionAdmin(MaskedPanMixin, admin.ModelAdmin):
    custom_fields = ['service_provider_id', 'service_info']
    readonly_fields = common_fields 
    search_fields = ['transaction_id', 'UUID']
    list_display = common_fields 
    fieldsets = (
        ('Morsal Information', {
            'fields': morsal_fields
        }),
        ('Transaction Information', {
            'fields': transaction_fields + ['service_provider_id', 'service_info']
        }),
        ('EBS Response', {
            'fields': response_fields
        }),
    )
    
class PurchaseTransactionAdmin(MaskedPanMixin, admin.ModelAdmin):
    custom_fields = ['service_provider_id', 'service_info']
    readonly_fields = common_fields 
    search_fields = ['transaction_id', 'UUID']
    list_display = common_fields 
    fieldsets = (
        ('Morsal Information', {
            'fields': morsal_fields
        }),
        ('Transaction Information', {
            'fields': transaction_fields + ['service_provider_id', 'service_info']
        }),
        ('EBS Response', {
            'fields': response_fields
        }),
    )
class BillPaymentTransactionAdmin(MaskedPanMixin, admin.ModelAdmin):
    custom_fields = ['personal_payment_info', 'payee_id','additional_data']
    readonly_fields = common_fields + custom_fields
    search_fields = ['transaction_id', 'UUID']
    list_display = common_fields + custom_fields
    fieldsets = (
        ('Morsal Information', {
            'fields': morsal_fields
        }),
        ('Transaction Information', {
            'fields': transaction_fields + ['service_provider_id', 'service_info']
        }),
        ('EBS Response', {
            'fields': response_fields
        }),
    )
admin.site.register(PaymentTransaction, PaymentTransactionAdmin)
admin.site.register(CardTransferTransaction, CardTransferTransactionAdmin)
admin.site.register(GenerateVoucherTransaction, GenerateVoucherTransactionAdmin)
admin.site.register(ServicePaymentTransaction, ServicePaymentTransactionAdmin)
admin.site.register(TopUpCardTransaction, TopUpCardTransactionAdmin)
admin.site.register(PurchaseTransaction, PurchaseTransactionAdmin)

admin.site.register(BillPaymentTransaction, BillPaymentTransactionAdmin)
