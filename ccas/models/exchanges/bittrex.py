import time
import hmac
import hashlib
import urllib
import urllib.request
import json
from decimal import *


def get_balances(public_key, secret_key):
    return_reposne = {}
    try:
        nonce = int(time.time() * 1000)

        request_url = 'https://bittrex.com/api/v1.1/account/getbalances?apikey='+ public_key.decode() +'&nonce=' + str(nonce)

        sign = hmac.new(secret_key, request_url.encode(), hashlib.sha512).hexdigest()

        headers = {
            "apisign": sign
        }

        req = urllib.request.Request(request_url, None, headers)
        with urllib.request.urlopen(req) as response:
            raw_json = response.read().decode("utf-8")

        parsed = json.loads(raw_json)

        tmp_parsed = {}

        for element in parsed['result']:
            if element['Balance'] > 0:
                tmp_parsed[element['Currency']] = element['Balance']


        max_entrys = len(tmp_parsed)
        all_balances = [([0] * 5) for i in range(max_entrys)]

        i = 0
        for currency, value in tmp_parsed.items():
            all_balances[i][0] = currency
            all_balances[i][1] = "Bittrex"
            all_balances[i][2] = round(Decimal(value), 8)

            if currency != "BTC":
                all_balances[i][3] = round(get_price(currency), 8)
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


def get_price(currency):
    raw_json = urllib.request.urlopen('https://bittrex.com/api/v1.1/public/getticker?market=btc-' + currency.lower())
    return Decimal(json.loads(raw_json.read().decode('utf-8'))['result']['Ask'])
