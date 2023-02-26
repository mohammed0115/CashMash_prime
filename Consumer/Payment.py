from django.shortcuts import render


import re
import requests
import datetime
import uuid

import json
import time

class Parser(object):
    def parse_payment_info(self, payment_info={}):
        output = ""
        try:

            for _ in payment_info.keys():
                output += "%s=%s/" % (_, payment_info[_])
            output = output[0:len(output) - 1]
        except Exception as e:
            print(e)
        return output


class Validator(object):
    def check_if_expiration_date_is_valid(self, expiration_date=None):
        expiration_date = str(expiration_date)
        REGEX = '^[0-9]{4}$'
        if not re.match(REGEX, expiration_date):
            return False
        if len(expiration_date) != 4:
            return False
        return True

    def check_expiration_date(self, expiration_date=None):
        """ ToDo: Fix check to incldue date until end of month, instead of first day of the month"""
        expiration_date = str(expiration_date)
        if self.check_if_expiration_date_is_valid(expiration_date=expiration_date) is False:
            return False
        expiration_date_check = datetime.datetime.strptime(expiration_date, "%y%m").date()
        today = datetime.datetime.utcnow().date()
        if expiration_date_check <= today:
            return False
        else:
            return True

    def check_card_number(self, card_number=None):
        REGEX = '^[0-9]{16,19}$'
        try:
            if re.match(REGEX, str(card_number)):
                return True
            else:
                return False
        except Exception as e:
            print(e)
        return False

    def check_amount(self, amount=None):
        REGEX = '^[0-9]+(\.){0,1}[0-9]+$'
        try:
            if re.match(REGEX, str(amount)):
                return True
            else:
                return False
        except Exception as e:
            print(e)
        return False

    def check_phone_number(self, phone_number=None):
        """ ToDo: Check for phone number"""
        pass
        return True


class Generator(object):
    def generate_uuid(self):
        return str(uuid.uuid4())

    def timestamp(self):
        return datetime.datetime.utcnow().strftime("%d%m%y%H%M%S")


class Controller(object):
    def __init__(self,
                 UUID=None,
                 tranCurrency=None):
        self.timeout = 10
        self.user_agent = "Mozilla/5.0 - EBS-Payment-Controller"
        self.application_id = Config.APPLICATION_ID
        self.API = Config.API
        if UUID is None:
            self.UUID = Generator().generate_uuid()
        else:
            self.UUID = UUID
        self.data = {"applicationId": self.application_id,
                     "tranDateTime": Generator().timestamp(),
                     "UUID": self.UUID}
        self.base_response = {"responseCode": "400",
                              "responseMessage": "Error",
                              "responseStatus": "Error"
                              }
        if tranCurrency is None:
            self.tranCurrency = Config.tranCurrency
        else:
            self.tranCurrency = tranCurrency

    def card_to_card_transfer(self,
                              from_card=None,
                              to_card=None,
                              amount=None,
                              IPIN=None,
                              expiration_date=None):
        response = self.base_response


        data = self.data
        data["tranCurrency"] = self.tranCurrency
        data["tranAmount"] = amount
        data["PAN"] = from_card
        data["toCard"] = to_card
        data["expDate"] = expiration_date
        data["applicationId"] = "SADAD"
        data["tranDateTime"] = datetime.datetime.now().strftime("%d%m%y%H%M%S")
        data["authenticationType"] = "00"
        data["IPIN"] = IPIN
#        print(data)
        resp = json.loads(requests.post(self.API + "/QAConsumer/doCardTransfer", json=data, verify=False).text)
        response["responseMessage"] = resp["responseMessage"]
        response["responseCode"] = resp["responseCode"]
        response["responseStatus"] = resp["responseStatus"]
        response["amount"] = resp["tranAmount"]
        response["balance"] = resp["balance"]
        response["PAN"] = resp["PAN"]
        response["toCard"] = resp["toCard"]
        response["tranDateTime"] = resp["tranDateTime"]
        response["acqTranFee"] = resp["acqTranFee"]
#        print(response)
        return resp

    def balance_inquiry_for_PAN(self,
                                PAN=None,
                                IPIN=None,
                                expiration_date=None):
        response = self.base_response

        if not Validator().check_card_number(card_number=PAN):
            response["responseMessage"] = "Invalid credit_card number"
            response["responseCode"] = 400
            response["responseStatus"] = "Error"
            return response

        if not Validator().check_if_expiration_date_is_valid(expiration_date=expiration_date):
            response["responseMessage"] = "Invalid expiration date"
            response["responseCode"] = 400
            response["responseStatus"] = "Error"
            return response

        if not Validator().check_expiration_date(expiration_date=expiration_date):
            response["responseMessage"] = "Already expired credit card"
            response["responseCode"] = 400
            response["responseStatus"] = "Error"
            return response

        data = self.data
        data["PAN"] = PAN
        data["expDate"] = expiration_date
        data["tranCurrency"] = self.tranCurrency
        data["authenticationType"] = "00"
        data["IPIN"] = IPIN
        print(data)
        resp = json.loads(requests.post(self.API + "/QAConsumer/getBalance", json=data, verify=False).text)
        response["responseMessage"] = resp["responseMessage"]
        response["responseCode"] = resp["responseCode"]
        response["responseStatus"] = resp["responseStatus"]
        response["balance"] = resp["balance"]
        print(response)
        return resp

    def balance_inquiry_for_phone_number(self,
                                         phone_number=None,
                                         IPIN=None):
        response = self.base_response
        if not Validator().check_phone_number(phone_number=phone_number):
            response["responseMessage"] = "Invalid phone number"
            response["responseCode"] = 400
            response["responseStatus"] = "Error"
            return response

        data = self.data
        data["tranCurrency"] = self.tranCurrency
        data["entityType"] = "Phone No"
        data["entityId"] = phone_number

        resp = json.loads(requests.post(self.API + "/MCSConsumer/getBalance", json=data).text)
        response["responseMessage"] = resp["responseMessage"]
        response["responseCode"] = resp["responseCode"]
        response["responseStatus"] = resp["responseStatus"]
        response["balance"] = resp["balance"]

        return resp

    def get_public_key(self):
        response = self.base_response
        data = {}
        data["applicationId"] = "SADAD"
        data["UUID"] = str(uuid.uuid4())
        data["tranDateTime"] = datetime.datetime.now().strftime("%d%m%y%H%M%S")
        
        resp = json.loads(requests.post(
            self.API + "/QAConsumer/getPublicKey", json=data, verify=False).text)
        response["responseMessage"] = resp["responseMessage"]
        response["responseCode"] = resp["responseCode"]
        response["responseStatus"] = resp["responseStatus"]
        response["pubKeyValue"] = resp["pubKeyValue"]
        response["UUID"]  = data["UUID"]
        print(data["UUID"])
        return response

    def is_server_alive(self):
        response = self.base_response
        data = {}
        data["applicationId"] = "SADAD"
        data["UUID"] = str(uuid.uuid4())
        data["tranDateTime"] = datetime.datetime.now().strftime("%d%m%y%H%M%S")
        resp = json.loads(requests.post(self.API + "/QAConsumer/isAlive", json=data, verify=False).text)
        response["responseMessage"] = resp["responseMessage"]
        response["responseCode"] = resp["responseCode"]
        response["responseStatus"] = resp["responseStatus"]

        return response

    def get_payees_list(self):
        response = self.base_response
        resp = json.loads(requests.post(
            self.API + "/QAConsumer/getPayeesList", json=self.data, verify=False).text)
        response["responseMessage"] = resp["responseMessage"]
        response["responseCode"] = resp["responseCode"]
        response["responseStatus"] = resp["responseStatus"]
        response["payees"] = resp["payees"]
        print(resp)
        return response

    def get_transaction_status(self,
                             original_transaction_UUID=None):
        response = self.base_response
        data = self.data
        data["originalTranUUID"] = original_transaction_UUID
        resp = json.loads(requests.post(
            self.API + "/QAConsumer/getTransactionStatus", json=data, verify=False).text)

        response["responseMessage"] = resp["responseMessage"]
        response["responseCode"] = resp["responseCode"]
        response["responseStatus"] = resp["responseStatus"]
        return response

    def account_to_account_transfer(self,
                                    from_account=None,
                                    to_account=None,
                                    expiration_date=None,
                                    amount=None,
                                    IPIN=None):

        data = self.data
        response = self.base_response
        data["PAN"] = from_account
        data["IPIN"] = IPIN
        data["toAccount"] = to_account
        data["tranAmount"] = amount
        data["expDate"] = expiration_date
        data["tranCurrency"] = self.tranCurrency

        resp = json.loads(requests.post(
            self.API + "/QAConsumer/doAccountTransfer", json=data, verify=False).text)
        response["responseCode"] = resp["responseCode"]
        response["responseStatus"] = resp["responseStatus"]
        response["responseMessage"] = resp["responseMessage"]
        return response
    
    def get_bill_by_card(self,
                         PAN=None,
                         IPIN=None,
                         payee_id=None,
                         payment_info=None,
                         expiration_date=None):
        data = self.data
        response = self.base_response
        data["PAN"] = PAN
        data["IPIN"] = IPIN
        data["payeeId"] = payee_id
        data["paymentInfo"] = payment_info
        data["expDate"] = expiration_date
        print(data)
        resp = json.loads(requests.post(
            self.API + "/QAConsumer/getBill", json=data, verify=False).text)
        response["responseCode"] = resp["responseCode"]
        response["responseStatus"] = resp["responseStatus"]
        response["responseMessage"] = resp["responseMessage"]
        response["billInfo"] = resp["billInfo"]
       # response["your_request"] = data
       # print(resp)
        return resp

    def pay_bill_by_card(self,
                         PAN=None,
                         IPIN=None,
                         payee_id=None,
                         amount=None,
                         payment_info=None,
                         expiration_date=None):
        data = self.data
        response = self.base_response

        data["PAN"] = PAN
        data["IPIN"] = IPIN
        data["tranAmount"] = amount
        data["payeeId"] = payee_id
        data["paymentInfo"] = payment_info
        data["expDate"] = expiration_date
        data["tranCurrency"] = self.tranCurrency
        print(data)

        resp = json.loads(requests.post(
            self.API + "/QAConsumer/payment", json=data, verify=False).text)
        response = resp
        print(resp)
        return response
       # response["your_request"] = data
        #response["responseCode"] = resp["responseCode"]
        #response["responseStatus"] = resp["responseStatus"]
        #response["responseMessage"] = resp["responseMessage"]
        #response["billInfo"] = resp["billInfo"]
        #response["balance"] = resp["balance"]
        #response["issuerTranFee"] = resp["issuerTranFee"]
        
    
    def generate_voucher(self,
                         amount=None,
                         phone_number=None,
                         PAN=None,
                         IPIN=None,
                         expiration_date=None,
                         ):

        data = self.data 
        response = self.base_response
        data["tranAmount"] =  amount
        data["voucherNumber"] = phone_number
        data["PAN"] = PAN
        data["IPIN"] = IPIN
        data["expDate"] = expiration_date
        print(data)
        resp = json.loads(requests.post(
            self.API + "/QAConsumer/generateVoucher", json=data, verify=False).text)
        response["responseCode"] = resp["responseCode"]
        response["responseStatus"] = resp["responseStatus"]
        response["responseMessage"] = resp["responseMessage"]
        response["voucherCode"] = resp["voucherCode"]
        response["balance"] = resp["balance"]
        response["voucherNumber"] = resp["voucherNumber"]
        response["fromAccount"] = resp["fromAccount"]
        print(resp)
        return resp
        
        
        
        

    