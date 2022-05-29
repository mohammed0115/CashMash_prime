
import re
import requests
import datetime
import uuid

import json
import time

import uuid
EBS_CONSUMER_API = {
    'END_POINT': 'https://172.16.199.1:8877/QAConsumer',
    'APPLICATION_ID': 'SADAD',
    'VERIFY_SSL': False,  # See line EBS_MERCHANT_API.VERIFY_SSL.
    'TIMEOUT': 60,  # 60 seconds
    'TIME_ZONE': 'Africa/Khartoum'  # This is used to parse datetime to the time zone EBS required
}

data = {}
data["applicationId"] = "SADAD"
data["UUID"] = str(uuid.uuid4())
data["tranDateTime"] = datetime.datetime.now().strftime("%d%m%y%H%M%S") 
resp = json.loads(requests.post(EBS_CONSUMER_API["END_POINT"]+ "/isAlive", json=data,timeout=60, verify=False).text)
response["responseMessage"] = resp["responseMessage"]
response["responseCode"] = resp["responseCode"]
response["responseStatus"] = resp["responseStatus"]
response["pubKeyValue"] = resp["pubKeyValue"]
response["UUID"]  = data["UUID"]
