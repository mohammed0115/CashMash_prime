from django.shortcuts import render
from rest_framework.response import Response
import requests
import json
from EBS_CONSUMER_API.models import ebs_consumer
# Create your views here.
class Ebs(object):
    services_list=['/getPublicKey',
                   '/register',
                   '/completeCardRegistration',
                   '/getBalance',
                   '/getBill',
                   '/payment',
                   '/doCardTransfer',
                   '/isAlive',
                   '/getPayeesList',
                   '/changeIPin',
                   '/changePassword',
                   '/forgetPassword',
                   '/adminResetPassword',
                   '/generateVoucher',
                   '/specialPayment',
                   '/getTransactionStatus',
                   '/updateRegisteredCard',
                   '/doAccountTransfer',
                   '/doMerchantsRegistration',
                   '/doQRPurchase',
                   '/doQRRefund',
                   '/getMerchantTransactions',
                   '/checkMsisdnAganistPAN',
                   '/completeTransaction',
                   '/getCustomerInfo',
                   '/doCashIn',
                   '/doCashOut',
                   '/getFileEncryptionKey',
                   '/getBatchStatus',
                   '/processFileBatch',
                   '/processOnlineBatch'
                   ]
    def post(self,endpoint,data):
        data["applicationId"] = ebs_consumer.objects.first().APPLICATION_ID
        resp = json.loads(requests.post(ebs_consumer.objects.first().END_POINT+ endpoint, json=data, verify=False).text)
        return resp
    def getPublicKey(self,tranDateTime,UUID):
        data = {}
        data["UUID"] = UUID
        data["tranDateTime"] = tranDateTime
        return self.post(self.services_list[0],data)
    def isAlive(self,tranDateTime,UUID):
        data = {}
        data["UUID"] = UUID
        data["tranDateTime"] = tranDateTime
        return self.post(self.services_list[0],data)
    def isAliAdminResetPasswordve(self,
                                  tranDateTime,
                                  UUID,
                                  userName,
                                  entityId,
                                  entityType,
                                  newUserPassword,
                                  adminUserName):

        data = {}
        data["UUID"] = UUID
        data["tranDateTime"] = tranDateTime
        data['userName'] =userName
        data['entityId'] =entityId
        data['entityType'] =entityType
        data['newUserPassword'] =newUserPassword
        data['adminUserName'] =adminUserName
        return self.post(self.services_list[2],data)
    def register_physical_standard(  self,
                            tranDateTime,
                            UUID,
                            PAN,
                            entityId,
                            entityType,
                            entityGroup,
                            userName,
                            userPassword,
                            phoneNo,
                            registrationType,
                            IPIN,
                            expDate,
                            mbr,
                            panCategory):
        data = {}
        data={
    #     "applicationId":"ITQAN",
        "entityId":entityId, 
        "entityType": entityType,
        "entityGroup": entityGroup, 
        "userName": userName, 
        "tranDateTime":tranDateTime,
        "UUID":UUID,
        "IPIN":IPIN,
        "userPassword":userPassword,
        "phoneNo": phoneNo, 
        "registrationType": registrationType,
        "PAN":PAN,
        "expDate": expDate, 
        #  "mbr": "0", 
        #  "panCategory": "Standard"
        }
        # data["UUID"] = UUID
        # data["tranDateTime"] = tranDateTime
        # data["PAN"] = PAN
        # data["entityId"] = entityId
        # data["entityType"] = entityType
        # data["entityGroup"] = entityGroup
        # data['userName']=userName
        # data["userPassword"] = userPassword
        # data["phoneNo"] = phoneNo
        # data["registrationType"] = registrationType
        # data["IPIN"] = IPIN
        # data['mbr']=mbr
        # data["panCategory"] = panCategory
        return self.post(self.services_list[1],data)
    def BalanceInquiry_auth11(self,
                            tranDateTime,
                            UUID,
                            PAN,
                            entityId,
                            entityType,
                            authenticationType,
                            userName,
                            userPassword,
                            fromAccountType,
                            expDate,
                            mbr,
                            tranCurrency
                            ):
        """
        {
        "tranDateTime": "190323161734", 
        "UUID": "d87b1f00-3fb7-4889-8b80-3608f4b2357a",
        "PAN": "9736441899952970",
        "expDate": "2303",
        "authenticationType": "11",
        "fromAccountType": "00",
        "tranCurrency": "SDG",
        "entityId": "249923592173",
        "entityType": "Phone No",
        "userName": "ITQANtest2037",
        "userPassword": "iVTcH8nhqAr83R35g+LY73hWA/d4wXy2C4wBCNR8iL8raHQhaDfqWRwEjX31VeaYxCtHwezV0mzuoV+KnY+Ynw==",
        "mbr": "0"
        }
        """

        data = {}
        data={
                "tranDateTime":tranDateTime, 
                "UUID": UUID,
                "PAN": PAN,
                "expDate": expDate,
                "authenticationType": authenticationType,
                "fromAccountType":fromAccountType,
                "tranCurrency": tranCurrency,
                "entityId": entityId,
                "entityType":entityType,
                "userName": userName,
                "userPassword":userPassword ,
                "mbr": mbr
        }      
    def BalanceInquiry_auth00(self,
                            tranDateTime,
                            UUID,
                            PAN,
                            authenticationType,
                            IPIN,
                            fromAccountType,
                            expDate,
                            mbr,
                            tranCurrency
                            ):
        """
        {
        "tranDateTime":tranDateTime,
        "UUID":str(uu),
        "PAN":"9736441899952970",
        "expDate":"2303",
        "IPIN":Ipin,
        "authenticationType": "00",
        "fromAccountType": "00",
        "tranCurrency": "SDG",
        "mbr": "0"
        }
        """

        data = {}
        data={
                "tranDateTime":tranDateTime, 
                "UUID": UUID,
                "PAN": PAN,
                "expDate": expDate,
                "authenticationType": authenticationType,
                "fromAccountType":fromAccountType,
                "tranCurrency": tranCurrency,
                "IPIN":IPIN,
                "mbr": mbr
        }
        
        return self.post(self.services_list[3],data)
    def register_virtual(  self,
                            tranDateTime,
                            UUID,
                            entityId,
                            entityType,
                            entityGroup,
                            userName,
                            phoneNo,
                            registrationType=None,
                            ):
        data = {}
        data["UUID"] = UUID
        data["tranDateTime"] = tranDateTime
        data["entityId"] = entityId
        data["entityType"] = entityType
        data["entityGroup"] = entityGroup
        data['userName']=userName
        data["phoneNo"] = phoneNo
        data["registrationType"] = "01"
        
        return self.post(self.services_list[1],data)
