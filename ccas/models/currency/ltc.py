import urllib
import urllib.request
import json
from decimal import *
from ccas.models import exchanges


def get_balance(list_of_address):
    return_reposne = {}
    # try:
    string_of_addresses = ''

    if isinstance(list_of_address[0], list):
        use_names = True
    else:
        use_names = False

    for address in list_of_address:
        if use_names:
            string_of_addresses = address[0] + ',' + string_of_addresses
        else:
            string_of_addresses = address + ',' + string_of_addresses

    req = urllib.request.Request('http://ltc.blockr.io/api/v1/address/balance/' + string_of_addresses[:-1], headers={'User-Agent': "Magic Browser"})
    con = urllib.request.urlopen(req)
    parsed = json.loads(con.read().decode('utf-8'))['data']
    #all_balances = [([0] * 6) for i in range(len(parsed))]

    all_balances = []
    price = Decimal(get_price())
    if isinstance(parsed, list):
        # multiple wallets
        i = 0
        for account in parsed:
            tmp_balances = []
            tmp_balances.append("LTC")
            tmp_balances.append(account['address'])
            tmp_balances.append(Decimal(account['balance']))
            tmp_balances.append(price)
            tmp_balances.append("CURRENCY")

            if use_names:
                tmp_balances.append(list_of_address[i][1])
            else:
                tmp_balances.append('')
            all_balances.append(tmp_balances)
            i += 1
    else:
        # one wallet
        tmp_balances = []
        tmp_balances.append("LTC")
        tmp_balances.append(parsed['address'])
        tmp_balances.append(Decimal(parsed['balance']))
        tmp_balances.append(price)
        tmp_balances.append("CURRENCY")

        if use_names:
            tmp_balances.append(list_of_address[0][1])
        else:
            tmp_balances.append('')
        all_balances.append(tmp_balances)

    return_reposne["status"] = True
    return_reposne["data"] = all_balances

    # except Exception as e:
    #     return_reposne["status"] = False
    #     return_reposne["msg"] = e

    return return_reposne

def get_price():
    return exchanges.get_price("LTC")
