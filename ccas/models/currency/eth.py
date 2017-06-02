import urllib
import urllib.request
import json
from decimal import *
from ccas.models import exchanges


def get_balance(list_of_address):
    return_reposne = {}
    try:
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


        raw_json = urllib.request.urlopen(
            'https://api.etherscan.io/api?module=account&action=balancemulti&address=' + string_of_addresses[:-1])
        parsed = json.loads(raw_json.read().decode('utf-8'))['result']

        all_balances = [([0] * 6) for i in range(len(parsed))]

        price = get_price()

        i = 0
        for account in parsed:
            all_balances[i][0] = "ETH"
            all_balances[i][1] = account['account']
            all_balances[i][2] = Decimal(account['balance']) / (10**18)
            all_balances[i][3] = price
            all_balances[i][4] = "CURRENCY"

            if use_names:
                all_balances[i][5] = list_of_address[i][1]
            else:
                all_balances[i][5] = ''

        return_reposne["status"] = True
        return_reposne["data"] = all_balances

    except Exception as e:
        return_reposne["status"] = False
        return_reposne["msg"] = e

    return return_reposne

def get_price():
    return exchanges.get_price("ETH")
