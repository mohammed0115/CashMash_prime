from django.shortcuts import render, redirect, HttpResponse

from django.http import JsonResponse

from api import EncriptIPIN
import re
import requests
import datetime
import uuid
from dateutil.tz import tzoffset
import json
import time
from rest_framework.decorators import api_view,authentication_classes,permission_classes
@api_view(['GET'])
@authentication_classes(())
@permission_classes(())
def index(request):
    return render(request,'index.html')

def error(request):
    return render(request,'error.html')
def success(request):
    return render(request,'success-payment.html')
def NotFound(request):
    return render(request,'404.html')
def transfer(request):
    if request.method == "POST":
        data = request.POST
        response = CardToCard_International(data['from_card_number'],data['from_card_expiry_date'],
        	int(data['from_card_cvv']),
         data['to_card_number'],
        	data['amount'])
        if response.status_code==200:
            response=response.json()
            if response['status']=="success":
                return render(request,"Pages/success-payment-transfer.html",{"result":response,"data":data})
            else:
                return render(request,"Pages/error.html",{"result":response})
        else:
            return render(request,"Pages/error.html",{"result":response})
    return render(request,'Pages/transfer.html',{"id":id})

def telecom(request):
    if request.method == "POST":
        sadad=EncriptIPIN.SADADTechBase()
        data = dict(request.POST)
        Ipin,uu=sadad.encryptIPIN("0000")
        data.update({
            "tranDateTime":str(datetime.datetime.now()),
            "UUID":uu,           
            "IPIN":Ipin,
            "authenticationType": "00",
            "mbr": 0,
            "paymentInfo": "MPHONE="+data['paymentInfo'],
            "fromAccountType": "00",
        })
        print("the request is:",data)
        result=sadad.Payment(**data)
        return render(request,'telecom.html',{})
    else:
        return render(request,'telecom.html',{})
def getbill(request):
    if request.method == "POST":
        sadad=EncriptIPIN.SADADTechBase()
        data = dict(request.POST)
        Ipin,uu=sadad.encryptIPIN("0000")
        data.update({
            "tranDateTime":str(datetime.datetime.now()),
            "UUID":uu,           
            "IPIN":Ipin,
            "authenticationType": "00",
            "mbr": 0,
            "paymentInfo": "MPHONE="+data['paymentInfo'],
            "fromAccountType": "00",
        })
        print("the request is:",data)
        result=sadad.Payment(**data)
        return render(request,'telecom.html',{})
    else:
        return render(request,'telecom.html',{})
        
    

def electricty(request):
    if request.method == "POST":
        data = request.POST
        return render(request,"Pages/error.html",{"result":response})

    return render(request,'Pages/electricty.html')

