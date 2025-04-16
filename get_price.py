import time
import requests
import hmac
from hashlib import sha256
from keys import APIKEY, SECRETKEY
from get_funds import get_funds

APIURL = "https://open-api.bingx.com"
APIKEY = APIKEY
SECRETKEY = SECRETKEY

def get_price(symbol: str, deposit_percent: int):

    funds = get_funds(deposit_percent)

    payload = {}
    path = '/openApi/swap/v2/quote/premiumIndex'
    method = "GET"
    paramsMap = {
    "symbol": f"{symbol}-USDT"
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload, funds)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload, funds):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    response = response.json()
    price = float(response["data"]["markPrice"])
    deal_price = funds / price
    print(funds, price)
    print(deal_price)
    return deal_price

def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "":
     return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
     return paramsStr+"timestamp="+str(int(time.time() * 1000))
