import time
import hmac
import hashlib
import urllib
import urllib.request
import json
from decimal import *

import collections

from . import keys


def get_balances(public_key, secret_key):
    return_reposne = {}
    try:
        req = {}
        req['command'] = "returnBalances"
        req['nonce'] = int(time.time() * 1000)

        post_data = str.encode(urllib.parse.urlencode(req))

        sign = hmac.new(secret_key, post_data, hashlib.sha512).hexdigest()
        headers = {
            'Sign': sign,
            'Key': public_key
        }

        req = urllib.request.Request('https://poloniex.com/tradingApi', post_data, headers)

        with urllib.request.urlopen(req) as response:
            raw_json = response.read().decode("utf-8")

        parsed = json.loads(raw_json)
        parsed = {key: value for key, value in parsed.items() if Decimal(value) > 0}

        max_entrys = len(parsed)
        all_balances = [([0] * 5) for i in range(max_entrys)]

        all_prices = get_all_prices()
        i = 0
        for currency, value in parsed.items():
            all_balances[i][0] = currency
            all_balances[i][1] = "Poloniex"
            all_balances[i][2] = Decimal(value)

            if currency != "BTC":
                all_balances[i][3] = Decimal(all_prices["BTC_" + currency]["highestBid"])
            else:
                all_balances[i][3] = 1

            all_balances[i][4] = "EXCHANGE"
            i += 1
        return_reposne["status"] = True
        return_reposne["data"] = all_balances

    except Exception as e:
        return_reposne["status"] = False
        return_reposne["msg"] = e

    return return_reposne

def get_all_prices():
    raw_json = urllib.request.urlopen('https://poloniex.com/public?command=returnTicker')
    return json.loads(raw_json.read().decode('utf-8'))

def get_price(currency):
    raw_json = urllib.request.urlopen('https://poloniex.com/public?command=returnOrderBook&currencyPair=BTC_'+ currency +'&depth=1')
    return Decimal(json.loads(raw_json.read().decode('utf-8'))["asks"][0][0])