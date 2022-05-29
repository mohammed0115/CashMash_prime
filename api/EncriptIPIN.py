import base64
from django.shortcuts import render, redirect, HttpResponse

import requests
import json

import rsa as rsa

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Cipher import PKCS1_v1_5
from base64 import b64decode,b64encode
import uuid as _uuid
# from FrontEnd.APIs import VendorAPIs,InvoiceAPIs,CustomerAPIs

class SADADTechBase():

    session = None
    base_url = 'http://45.77.252.45/'

    def __init__(self):
        pass
    def Payment(sefl,PAN,  IPIN, expDate,tranDateTime,UUID,payeeId,paymentInfo,authenticationType,fromAccountType,tranAmount):
        
        return self.request('Payment',
                            'POST',
                            PAN=PAN,
                            IPIN=IPIN,
                            expDate=expDate,
                            tranDateTime=tranDateTime,
                            UUID=UUID,
                            payeeId=payeeId,
                            paymentInfo=paymentInfo,
                            authenticationType=authenticationType,
                            tranAmount=tranAmount,
                            fromAccountType=fromAccountType)
    def getbill(self,PAN,  IPIN, expDate,tranDateTime,UUID,payeeId,paymentInfo,authenticationType):
    
        return self.request('GetBill',
                            'POST',
                            PAN=PAN,
                            IPIN=IPIN,
                            expDate=expDate,
                            tranDateTime=tranDateTime,
                            UUID=UUID,
                            payeeId=payeeId,
                            paymentInfo=paymentInfo,
                            authenticationType=authenticationType
                            )

    def transactionStatus(self,tranDateTime,UUID,originalTranUUID):
    	return self.request('TransactionStatus',
                            'POST',
                            
                            tranDateTime=tranDateTime,
                            UUID=UUID,
                            originalTranUUID=originalTranUUID
                            
                            
                            
                            )
    def payeelist(self,tranDateTime,UUID):
    	return self.request('PayeeList',
                            'POST',
                            tranDateTime=tranDateTime,
                            UUID=UUID 
                            )
                             
    def card_to_card_transfer(self
                              ,PAN,  
                              IPIN,
                              toCard,
                              expDate,
                              authenticationType,
                              toAccountType,
                              tranDateTime,
                              UUID,
                              fromAccountType,
                              tranCurrency,
                              mbr,
                              tranAmount):

        return self.request('CardTransfer',
                            'POST',
                            PAN=PAN,
                            IPIN=IPIN,
                            toCard=toCard,
                            expDate=expDate,
                            authenticationType=authenticationType,
                            toAccountType=toAccountType,
                            tranDateTime=tranDateTime,
                            UUID=UUID,
                            fromAccountType=fromAccountType,
                            tranCurrency=tranCurrency,
                            mbr=mbr,                            
                            tranAmount=tranAmount
                            
                            
                            )
    def Balance(self,PAN,  IPIN, expDate,authenticationType,tranDateTime,UUID,fromAccountType,tranCurrency,mbr):
    
        return self.request('BalanceInquiry',
                            'POST',
                            PAN=PAN,
                            authenticationType=authenticationType,
                            IPIN=IPIN,
                            expDate=expDate,
                            tranDateTime=tranDateTime,
                            fromAccountType=fromAccountType,
                            tranCurrency=tranCurrency,
                            mbr=mbr,
                            UUID=UUID
                            )

    def request(self,endpoint,method,**params):

        url = str(self.base_url)+str(endpoint)+"/"

        payload = json.dumps(params)
        headers = {
            'content-type': "application/json",
           
            # 'postman-token': "8596a3c8-7b4b-ebaa-8e98-26ebca3d6f57"
        }
        # Enaya=CustomerAPIs()
        # cookies = dict(sessionid=Enaya.getSession(pk)['Sessionid'])

        print("method",method)
        print("url",url)
        print("data",payload)
        print("headers",headers)
        # print("cookies",cookies)

        response = requests.request(method.upper(), url, data=payload, headers=headers)
        print(response.text)
        try:
            if response.status_code==200:
                return json.loads(response.text)
            elif response.status_code==404:
                return redirect('NotFound')
            else:
                return redirect('NotFound')
        except Exception as e:
            raise Exception("Enayatech is responded with error : "+response.text)


    def encryptIPIN(self,ipin):

        endpoint = 'GetPublicKey'
        res = self.request(endpoint, "POST",IPIN=ipin)
        print(res)
        pubKey = res.get('pubKeyValue')
        print(pubKey)
        uuid = str(_uuid.uuid4())

        return self.generateEncrypted(ipin,pubKey,uuid).decode('utf-8'),uuid


    def generateEncrypted(self,ipin,publicKey,uuid):

        data = uuid + ipin
        

        pubkey = publicKey
        msg = data
        keyDER = b64decode(pubkey)
        keyPub = RSA.importKey(keyDER)
        cipher = Cipher_PKCS1_v1_5.new(keyPub)
        cipher_text = cipher.encrypt(msg.encode())
        emsg = b64encode(cipher_text)
        print (emsg)

        message = data.encode('utf8')
        crypto = base64.b64encode(rsa.encrypt(message, keyPub))  # encodes encrypted message in Base64 also
        return crypto
