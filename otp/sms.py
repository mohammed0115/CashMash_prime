import requests


def _convert_mobile_number(mobile_number):
        if mobile_number.startswith("249"):
            return mobile_number
        return "249" + mobile_number[1:]

def sms(message,phone):
    print(phone)
    url = "http://212.0.129.229/bulksms/webacc.aspx?user=sadad&pwd=806807&smstext="+message+"&Sender=sadad&Nums="+_convert_mobile_number(phone)
    payload={}
    headers = {
  		'Content-Type': 'application/json'
	}
    return requests.request("GET", url, headers=headers, data=payload)
	
# print(sms(message,phone),"lll")
