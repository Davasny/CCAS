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
        req = {}
        req['method'] = "getInfo"
        req['nonce'] = get_last_nonce(public_key, secret_key)+1

        post_data = str.encode(urllib.parse.urlencode(req))

        sign = hmac.new(secret_key, post_data, hashlib.sha512).hexdigest()

        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Sign": sign,
            "Key": public_key
        }

        req = urllib.request.Request('https://btc-e.com/tapi', post_data, headers)
        with urllib.request.urlopen(req) as response:
            raw_json = response.read().decode("utf-8")

        parsed = json.loads(raw_json)

        parsed = {key: value for key, value in parsed['return']['funds'].items() if Decimal(value) > 0}

        max_entrys = len(parsed)
        all_balances = [([0] * 5) for i in range(max_entrys)]

        #all_prices = get_all_prices()

        i = 0
        for currency, value in parsed.items():
            all_balances[i][0] = currency
            all_balances[i][1] = "BTC-e"
            all_balances[i][2] = round(Decimal(value), 8)

            if currency != "btc" and currency != 'usd':
                all_balances[i][3] = round(get_price(currency), 8)
            elif currency == "usd":
                all_balances[i][3] = round(1/get_btc_price(), 8)
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


def get_last_nonce(public_key, secret_key):
    req = {}
    req['method'] = "getInfo"
    req['nonce'] = 1
    post_data = str.encode(urllib.parse.urlencode(req))

    sign = hmac.new(secret_key, post_data, hashlib.sha512).hexdigest()

    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Sign": sign,
        "Key": public_key
    }

    req = urllib.request.Request('https://btc-e.com/tapi', post_data, headers)

    with urllib.request.urlopen(req) as response:
        raw_json = response.read().decode("utf-8")

    return int(json.loads(raw_json)['error'].split(":")[3])


def get_price(currency):
    raw_json = urllib.request.urlopen('https://btc-e.com/api/3/ticker/' + currency.lower() + '_btc')
    return Decimal(json.loads(raw_json.read().decode('utf-8'))[currency.lower() + '_btc']['buy'])


def get_btc_price():
    raw_json = urllib.request.urlopen('https://btc-e.com/api/3/ticker/btc_usd')
    return Decimal(json.loads(raw_json.read().decode('utf-8'))['btc_usd']['buy'])