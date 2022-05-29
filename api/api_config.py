import requests
import json
import base64
import rsa as rsa
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Cryptodome.Cipher import PKCS1_v1_5
from base64 import b64decode, b64encode
import uuid as _uuid
import uuid
from api.models import User
def _convert_mobile_number(mobile_number):
        if mobile_number.startswith("+"):
            return mobile_number[1:]
        else:
            return mobile_number
def converExpirydate2DB(value):
        x="/"
        expirydateDB=None
        if x in value:
          i=value.index(x)
          month = value[:i]
          year  = value[(i+1):]
          if month.isdigit() and year.isdigit():
            tar=[1,2,3,4,5,6,7,8,9,10,11,12]
            if len(month)==1:
                if int(month) in tar:
                    month="0"+month
                    expirydateDB=year+month
            elif len(month)==2 and int(month) in tar :
                expirydateDB=year+month
        return expirydateDB
def get_url():
    base_url = "https://api.enayapay.com/api/v2.0/confirm_order/"
    return base_url


def get_header():
    # if User.objects.filter(id=id).exists():
    #     token=User.objects.get(id=id).token
    #     if token:
    #         headers = {
    #             'x-api-key': '8317b047-7465-4327-b613-19169fc6abe7',
    #             'token':token,
    #             'Content-Type': 'application/json'
    #             }
    #     else:
    #         headers = {
    #             'x-api-key': '8317b047-7465-4327-b613-19169fc6abe7',
    #             'token':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImJha2hlZXQiLCJleHBpcnkiOiIyMDIxLTAxLTI4In0.sG87nVzJ3ECWCAB8uB-muEfYLhl3IoXaltkFTDG8G8s',
    #             'Content-Type': 'application/json'
    #                 }
    # else:
    headers = {
                'x-api-key': '8317b047-7465-4327-b613-19169fc6abe7',
                'token':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImJha2hlZXQiLCJleHBpcnkiOiIyMDIxLTAxLTI4In0.sG87nVzJ3ECWCAB8uB-muEfYLhl3IoXaltkFTDG8G8s',
                'Content-Type': 'application/json'
                    }
    return headers

def pay_bill_by_card(payee_id,card_number,cvv,payment_info,amount,expiration_date):
    base_url = "https://api.enayapay.com/api/v2.0/pay_bill/"
    body={
            "PAN": card_number,
            "IPIN": str(cvv),
            "payee_id": str(payee_id),
            "payment_info": "MPHONE ="+payment_info+"",
            "expiration_date": converExpirydate2DB(expiration_date),
            "amount": amount,
            "platform":"web"

    }
    print("data well pay is :",body)
    response = requests.request(
        'POST', base_url, headers=get_header(), json=body)
    print(response.text)
    return response

def pay_bill_by_card1(payee_id,card_number,cvv,payment_info,amount,expiration_date):
    base_url = "https://api.enayapay.com/api/v2.0/pay_bill/"
    body={
            "PAN": card_number,
            "IPIN": cvv,
            "payee_id": str(payee_id),
            "payment_info": "METER="+payment_info+"",
            "expiration_date": converExpirydate2DB(expiration_date),
            "amount": amount,
            "platform":"web"

    }
    print("data well pay is :",body)
    response = requests.request(
        'POST', base_url, headers=get_header(), json=body)
    print(response.text)
    return response

def addCard(pan,expiry_date,default):
     base_url = "https://api.enayapay.com/api/v2.0/confirm_order/add_card/"
     body={"pan":pan,"expiry_date":expiry_date,"default":default}
     response = requests.request('POST', base_url, headers=get_header(), json=body)
     return response


def CardToCard_Local(from_card_number,
    from_card_expiry_date,
    to_card_number,amount_sdg,iPIN):
        Base_url="https://api.enayapay.com/api/v2.0/card_to_card/"
        headers ={
                'Content-Type': 'application/json',
                'x-api-key': "8317b047-7465-4327-b613-19169fc6abe7",
                'token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImJha2hlZXQiLCJleHBpcnkiOiIyMDIxLTAxLTI4In0.sG87nVzJ3ECWCAB8uB-muEfYLhl3IoXaltkFTDG8G8s"
            }
        #http://pay.int.live.enayatech.com/api/
        print("int cvv------------->[",headers)
        body={
                "from_card": str(from_card_number),
                "IPIN":iPIN,
                "to_card":str(to_card_number),
                # "exp_year": str(from_card_expiry_date)[:2],
                # "exp_month":str(from_card_expiry_date)[2:],
                "platform":"web",
                # "payment_type":"card_to_card",
                "amount": amount_sdg,
              
                "IPIN":iPIN,
                "expiration_date":str(from_card_expiry_date),
                "UUID":str(_uuid.uuid4())
            }
        print("data well pay is ",body)
        response=requests.request("POST", Base_url, headers=headers, json = body)
        print(response.text)
        return response


def CardToCard_International(from_card_number,from_card_expiry_date,from_card_cvv,to_card_number,amount_sdg):
    Base_url="https://api.enayapay.com/api/v2.0/card_to_card/"
    headers = {
                'Content-Type': 'application/json',
                'x-api-key': "8317b047-7465-4327-b613-19169fc6abe7",
                'token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImJha2hlZXQiLCJleHBpcnkiOiIyMDIxLTAxLTI4In0.sG87nVzJ3ECWCAB8uB-muEfYLhl3IoXaltkFTDG8G8s"
            }
        #http://pay.int.live.enayatech.com/api/
    print("int cvv------------->[",headers)
    body={

                "from_card": str(from_card_number),
                "to_card":str(to_card_number),
                "IPIN":from_card_cvv,
                "platform":"web",
                "amount": amount_sdg,        
                "expiration_date":converExpirydate2DB(from_card_expiry_date),
                "UUID":str(uuid.uuid4())

            }
    print("data well pay is :",body)
    response=requests.request("POST", Base_url, headers=headers, json = body)
    print(response.text)
    return response


def registerUser(name,phone_number):
    Base_url="https://api.enayapay.com/api/v2.0/register/"
    headers = {
                'Content-Type': 'application/json',
                'x-api-key': "8317b047-7465-4327-b613-19169fc6abe7",
                'token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImJha2hlZXQiLCJleHBpcnkiOiIyMDIxLTAxLTI4In0.sG87nVzJ3ECWCAB8uB-muEfYLhl3IoXaltkFTDG8G8s"
            }
    body={
        "phone_number":_convert_mobile_number(phone_number),
        "name":name

        }
    response=requests.request("POST", Base_url, headers=headers, json = body)
    print(response.text)
    return response


def loginUser(phone_number):
    Base_url="https://api.enayapay.com/api/v2.0/login/"
    headers = {
                'Content-Type': 'application/json',
                'x-api-key': "8317b047-7465-4327-b613-19169fc6abe7",
                'token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImJha2hlZXQiLCJleHBpcnkiOiIyMDIxLTAxLTI4In0.sG87nVzJ3ECWCAB8uB-muEfYLhl3IoXaltkFTDG8G8s"
            }
    body={
        "phone_number":_convert_mobile_number(phone_number),


        }
    r=requests.request("POST", Base_url, headers=headers, json = body)
    print(r.text)
    return r



def verify(totp,phone_number):
    Base_url="https://api.enayapay.com/api/v2.0/verify/"
    headers = {
                'Content-Type': 'application/json',
                'x-api-key': "8317b047-7465-4327-b613-19169fc6abe7",
                'token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImJha2hlZXQiLCJleHBpcnkiOiIyMDIxLTAxLTI4In0.sG87nVzJ3ECWCAB8uB-muEfYLhl3IoXaltkFTDG8G8s"
            }
    body={
        "phone_number":_convert_mobile_number(phone_number),
        "totp":totp

        }
    response=requests.request("POST", Base_url, headers=headers, json = body)
    print(response.text)
    return response
