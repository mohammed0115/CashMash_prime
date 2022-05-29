from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .EBS_Request import EBSRequestAPIView
from .serializers import BaseConsumerAPISerializer,CardTransferAPISerializer

import re
import requests
import datetime
import uuid

import json
import time

import uuid

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend

from .models import PaymentTransaction, GenerateVoucherTransaction, ServicePaymentTransaction, \
    CardTransferTransaction
from .models import TopUpCardTransaction

from .permissions import HasValidAPIKey, IsCardHolderUser
from .serializers import CardHolderTopUpTransactionRetrieveSerializer, CardTransferAPISerializer, \
    GenerateVoucherConsumerAPISerializer, ServicePaymentConsumerAPISerializer, BillInquiryConsumerAPISerializer, \
    PaymentConsumerAPISerializer, TransactionStatusConsumerAPISerializer,\
        BaseConsumerAPISerializer,CardBalanceInquirySerializer,ChangeCardsIpin,\
            RegisterSerializer,QRPurchaseSerializer,QRRefundSerializer,CompletecardregistrationSerializer,\
                ChangePasswordSerializer,ForgetPasswordSerializer
    
from .filters import IsTopUpTransactionCardOwnerFilterBackend, TopUpTransactionFilter
from .authentication import CardHolderAccessTokenAuthentication
from .pagination import LargeResultsSetPagination
# from apps.api_utilities.ebs_api import views as ebs_views, serializers as ebs_serializers
from django.conf import settings
from pytz import timezone
# from datetime import datetime
from django.conf import settings
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from CardManagement.serializers import VirtualCardSerializer
base_response = {"responseCode": "400",
                              "responseMessage": "Error",
                              "responseStatus": "Error"
                              }
@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def get_public_key(request):
        response = base_response
        data = {}
        data["applicationId"] = "SADAD"
        data["UUID"] = str(uuid.uuid4())
        data["tranDateTime"] = datetime.datetime.now().strftime("%d%m%y%H%M%S")
        
        resp = json.loads(requests.post(
            settings.EBS_CONSUMER_API["END_POINT"]+ "/getPublicKey", json=data, verify=False).text)
        response["responseMessage"] = resp["responseMessage"]
        response["responseCode"] = resp["responseCode"]
        response["responseStatus"] = resp["responseStatus"]
        response["pubKeyValue"] = resp["pubKeyValue"]
        response["UUID"]  = data["UUID"]
        print(data["UUID"])
        return Response(response)
@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def echoTest(request):
        response = base_response
        data = {}
        data["applicationId"] = "SADAD"
        data["UUID"] = str(uuid.uuid4())
        data["tranDateTime"] = datetime.datetime.now().strftime("%d%m%y%H%M%S")
        
        resp = json.loads(requests.post(
            settings.EBS_CONSUMER_API["END_POINT"]+ "/isAlive", json=data, verify=False).text)
        # response["responseMessage"] = resp["responseMessage"]
        # response["responseCode"] = resp["responseCode"]
        # response["responseStatus"] = resp["responseStatus"]
        # response["pubKeyValue"] = resp["pubKeyValue"]
        # response["UUID"]  = data["UUID"]
        # print(data["UUID"])
        return Response(resp)
@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def balance_inquiry_for_PAN(request):
    
        request_data = dict(request.data)
        data={
            "authenticationType": "00",
            "fromAccountType": "00",
            "tranCurrency": "SDG",
            "mbr": "0"
        }
        data["applicationId"] = "SADAD"
        data["PAN"] = request_data["PAN"]
        data["expDate"] = request_data["expDate"]
        data["tranCurrency"] = request_data["tranCurrency"]
        data['UUID']=request_data["UUID"]
        data["IPIN"] = request_data["IPIN"]
        data["tranDateTime"] = request_data["tranDateTime"]
        
        print(data)
        resp = json.loads(requests.post(settings.EBS_CONSUMER_API["END_POINT"]+ "/getBalance", json=data, verify=False).text)
        # response["responseMessage"] = resp["responseMessage"]
        # response["responseCode"] = resp["responseCode"]
        # response["responseStatus"] = resp["responseStatus"]
        # response["balance"] = resp["balance"]
        # print(response)
        return Response(resp)
class BaseConsumerTransactionView(EBSRequestAPIView):
    # key is the model fields name, value is the field name in EBS
    common_transaction_request_fields = {'transaction_date_time': 'tranDateTime',
                                         'uuid': 'UUID',
                                         'source_PAN': 'PAN',
                                         'transaction_amount': 'tranAmount',
                                         }

    common_transaction_response_fields = {'transaction_currency': 'tranCurrency',
                                          'from_account_type': 'fromAccountType',
                                          'from_account': 'fromAccount',
                                          'account_currency': 'accountCurrency',
                                          'issuer_fee': 'issuerTranFee',
                                          'acquirer_fee': 'acqTranFee',
                                          'response_message': 'responseMessage',
                                          'response_code': 'responseCode',
                                          'response_status': 'responseStatus',
                                          'balance': 'balance',
                                          'mbr': 'mbr',
                                          }

    transaction_model_class = None

    def get_transaction_request_fields(self):
        return self.common_transaction_request_fields

    def get_transaction_response_fields(self):
        return self.common_transaction_response_fields

    def pre_handle_200_ebs_response(self, response_data):
        # 1. Generate transaction ID
        transaction_id = str(uuid.uuid4())

        # 2. Return the transaction ID to the client
        response_data['transactionId'] = transaction_id

        # 3. Get user details
        user_id = self.request.user.id
        user_mobile_number = self.request.user.card_holder_mobile_number

        # 4. Log Transaction
        transaction_record = {'transaction_id': transaction_id}
        transaction_request_fields = self.get_transaction_request_fields()
        transaction_response_fields = self.get_transaction_response_fields()
        transaction_record["user_id"] = user_id
        transaction_record["user_mobile_number"] = user_mobile_number

        for key, value in transaction_request_fields.items():
            transaction_record[key] = self.validated_data.get(value, None)

        for key, value in transaction_response_fields.items():
            transaction_record[key] = response_data.get(value, None)

        self.transaction_model_class.objects.create(**transaction_record)


        return response_data


class TopUpTransactionViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    The view to return a list of Distributor top up transactions for a card holder. Transactions should be readonly.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = CardHolderTopUpTransactionRetrieveSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = (DjangoFilterBackend, IsTopUpTransactionCardOwnerFilterBackend)
    filter_class = TopUpTransactionFilter
    queryset = TopUpCardTransaction.objects.get_queryset().order_by('-tranDateTime')


class CardTransferView(EBSRequestAPIView):
    """
    Transfer money from one card to the other.
    This implements the request 3.8 'Card Transfer' in
    the EBS 'Multi-Channel support - Consumer' API documentation.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = CardTransferAPISerializer
    ebs_service_path = 'doCardTransfer'
    transaction_model_class = CardTransferTransaction

    def get_transaction_request_fields(self):
        fields = {}
        fields.update(self.common_transaction_request_fields)
        fields.update({'to_card': 'toCard', 'to_account_type': 'toAccountType'})
        return fields

    def get_transaction_response_fields(self):
        fields = {}
        fields.update(self.common_transaction_response_fields)
        # fields.update({'to_account': 'toAccount'})
        return fields

# def get_public_key(request):
#     x = PaymentController.Controller().get_public_key()
#     return JsonResponse(x)

class GenerateVoucherView(EBSRequestAPIView):
    """
    Used to generate a voucher code that can be cashed out through ATM/POS.
    This implements the request 3.14 'Generate Voucher' in
    the EBS 'Multi-Channel support - Consumer' API documentation.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = GenerateVoucherConsumerAPISerializer
    ebs_service_path = 'generateVoucher'
    transaction_model_class = GenerateVoucherTransaction

    def get_transaction_request_fields(self):
        fields = {}
        fields.update(self.common_transaction_request_fields)
        fields.update({'voucher_number': 'voucherNumber'})
        return fields

    def get_transaction_response_fields(self):
        fields = {}
        fields.update(self.common_transaction_response_fields)
        fields.update({'voucher_code': 'voucherCode'})
        return fields


class ServicePaymentView(EBSRequestAPIView):
    """
    Used to obtain special payment service / e-commerce payment.
    This implements the request 3.15 'Service Payment' in
    the EBS 'Multi-Channel support - Consumer' API documentation.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = ServicePaymentConsumerAPISerializer
    ebs_service_path = 'specialPayment'
    transaction_model_class = ServicePaymentTransaction

    def get_transaction_request_fields(self):
        fields = {}
        fields.update(self.common_transaction_request_fields)
        fields.update({'service_provider_id': 'serviceProviderId', 'service_info': 'serviceInfo'})
        return fields


class GetPayeeList(EBSRequestAPIView):
    """
    Send a message to EBS to get list of payees available in the system.
    This implements the request 3.3 'Payees List' in
    the EBS 'Multi-Channel support - Consumer' API documentation.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = BaseConsumerAPISerializer
    ebs_service_path = 'getPayeesList'


class GetBill(EBSRequestAPIView):
    """
    Send a message to EBS to get bill information for a specific customer accounts.
    This implements the request 3.5 'Bill Inquiry' in
    the EBS 'Multi-Channel support - Consumer' API documentation.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = BillInquiryConsumerAPISerializer
    ebs_service_path = 'getBill'


class PaymentView(EBSRequestAPIView):
    """
    Send a message to EBS to pay a bill or top up customer account for one of the billers (from Get Bill)
    This implements the request 3.6 'Payment' in
    the EBS 'Multi-Channel support - Consumer' API documentation.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = PaymentConsumerAPISerializer
    ebs_service_path = 'payment'
    transaction_model_class = PaymentTransaction

    def get_transaction_request_fields(self):
        fields = {}
        fields.update(self.common_transaction_request_fields)
        fields.update({'payee_id': 'payeeId',
                       'payment_info': 'paymentInfo'})
        return fields

    def get_transaction_response_fields(self):
        fields = {}
        fields.update(self.common_transaction_response_fields)
        fields.update({'bill_info': 'billInfo'})
        return fields


class TransactionStatusView(EBSRequestAPIView):
    """
    Send a request to EBS to get status of specific transaction.
    This implements the request 3.16 'Transaction Status' in
    the EBS 'Multi-Channel support - Consumer' API documentation.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = TransactionStatusConsumerAPISerializer
    ebs_service_path = 'getTransactionStatus'

    def get_response_data(self, ebs_response_content_json):
        ebs_response_content_json = super(TransactionStatusView, self).get_response_data(ebs_response_content_json)
        if 'originalTransaction' in ebs_response_content_json:
            app_id = ebs_response_content_json['originalTransaction'].get('applicationId')
            if app_id:
                del ebs_response_content_json['originalTransaction']['applicationId']

        return ebs_response_content_json
    




































# class GetPublicKeyView(BaseConsumerTransactionView):
#     """
#     Request the encryption key to use to encrypt PIN block.
#     This implements the request 3.4 'Get Public Key' in
#     the EBS 'Multi-Channel support - Consumer' API documentation.
#     """
#     permission_classes = ()
#     authentication_classes = ()
#     serializer_class = BaseConsumerAPISerializer
#     ebs_service_path = 'getPublicKey'
    
class PayeeListView(EBSRequestAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = BaseConsumerAPISerializer
    ebs_service_path = 'getPayeesList'
class EchoTestView(EBSRequestAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = BaseConsumerAPISerializer
    ebs_service_path = 'isAlive'
# # class doCardTransferView(EBSRequestAPIView):
# #     serializer_class = CardTransferAPISerializer
#     ebs_service_path = 'doCardTransfer'



class BalanceInquiryView(EBSRequestAPIView):
    """
    Request card balance.
    This implements the request 3.9 'Balance Inquiry' in
    the EBS 'Multi-Channel support - Consumer' API documentation.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = CardBalanceInquirySerializer
    ebs_service_path = 'getBalance'


class RequestPinChangeView(EBSRequestAPIView):
    """
    Request to change the IPIN for a card.
    This implements the request 3.10 'Change IPIN' in
    the EBS 'Multi-Channel support - Consumer' API documentation.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = ChangeCardsIpin
    ebs_service_path = 'changeIPin'
    
    
    
class register(EBSRequestAPIView):
    #RegisterSerializer
    permission_classes = ()
    authentication_classes = ()
    serializer_class = RegisterSerializer
    ebs_service_path = 'register'
class completeCardRegistration(EBSRequestAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = CompletecardregistrationSerializer
    ebs_service_path = 'completeCardRegistration'
class changePassword(EBSRequestAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = ChangePasswordSerializer
    ebs_service_path = 'changePassword'
class forgetPassword(EBSRequestAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = ForgetPasswordSerializer
    ebs_service_path = 'forgetPassword'
    


class VirtualCard(EBSRequestAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = VirtualCardSerializer
    ebs_service_path = 'register'








class doQRRefund(EBSRequestAPIView):
    permission_classes = (HasValidAPIKey,)
    authentication_classes = ()
    serializer_class = QRRefundSerializer
    ebs_service_path = 'doQRRefund'
class doQRPurchase(EBSRequestAPIView):
    permission_classes = (HasValidAPIKey,)
    authentication_classes = ()
    serializer_class = QRPurchaseSerializer
    ebs_service_path = 'doQRPurchase'
    
    
    


    
