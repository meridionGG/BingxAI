import time
import requests
import hmac
from hashlib import sha256
from keys import APIKEY, SECRETKEY

APIURL = "https://open-api.bingx.com"
APIKEY = APIKEY
SECRETKEY = SECRETKEY

def get_funds(deposit_percent: int):
    payload = {}
    path = '/openApi/account/v1/allAccountBalance'
    method = "GET"
    paramsMap = {
    "accountType": "USDTMPerp",
    "recvWindow": "6000",
    "timestamp": int((time.time()*1000))
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload, deposit_percent)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload, deposit_percent):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    response = response.json()
    funds = float(response["data"][0]["usdtBalance"])
    funds = funds * deposit_percent / 100
    return funds

def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "":
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))

# get_funds(1)