import time
import hmac
import hashlib
import urllib
import urllib.request
import json
from decimal import *
import base64


def get_balances(public_key, secret_key):
    return_reposne = {}
    try:
        req = {}
        req['request'] = "/v1/balances"
        req['nonce'] = str(time.time() * 1000)

        j = json.dumps(req)
        post_data = base64.standard_b64encode(j.encode('utf8'))

        #post_data = str.encode(urllib.parse.urlencode(req))

        sign = hmac.new(secret_key, post_data, hashlib.sha384).hexdigest()
        headers = {
            'X-BFX-SIGNATURE': sign,
            'X-BFX-PAYLOAD': post_data,
            'X-BFX-APIKEY': public_key
        }

        req = urllib.request.Request('https://api.bitfinex.com/v1/balances', post_data, headers)


        with urllib.request.urlopen(req) as response:
            raw_json = response.read().decode("utf-8")

        #[{"type":"exchange","currency":"eth","amount":"0.029","available":"0.029"}]
        if raw_json:
            parsed = json.loads(raw_json)

            parsed_tmp = {}
            for element in parsed:
                parsed_tmp[element['currency']] = element['amount']

            #parsed = {key: value for key, value in parsed.items() if Decimal(value) > 0}

            max_entrys = len(parsed_tmp)
            all_balances = [([0] * 5) for i in range(max_entrys)]

            i = 0
            for currency, value in parsed_tmp.items():
                all_balances[i][0] = currency
                all_balances[i][1] = "Bitfinex"
                all_balances[i][2] = Decimal(value)

                if currency != "btc" and currency != "usd":
                    all_balances[i][3] = Decimal(get_price(currency))
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


def get_price(currency):
    try:
        raw_json = urllib.request.urlopen('https://api.bitfinex.com/v1/pubticker/' + currency + 'btc')
        price = Decimal(json.loads(raw_json.read().decode('utf-8'))["ask"])
    except:
        price = -1
    return price


def get_btc_price():
    raw_json = urllib.request.urlopen('https://api.bitfinex.com/v1/pubticker/btcusd')
    return Decimal(json.loads(raw_json.read().decode('utf-8'))["ask"])
