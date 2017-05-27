import urllib
import urllib.request
import json
from decimal import *
from ccas.models.exchanges import poloniex


def get_balance(list_of_address):
    string_of_addresses = ''
    for address in list_of_address:
        string_of_addresses = address + ',' + string_of_addresses

    raw_json = urllib.request.urlopen(
        'https://api.etherscan.io/api?module=account&action=balancemulti&address=' + string_of_addresses[:-1])
    parsed = json.loads(raw_json.read().decode('utf=8'))

    all_balances = [([0] * 5) for i in range(len(parsed))]

    price = get_price()

    i = 0
    for account in parsed:
        all_balances[i][0] = "ETH"
        all_balances[i][1] = parsed['result'][i-1]['account']
        all_balances[i][2] = Decimal(parsed['result'][i-1]['balance']) / (10**18)
        all_balances[i][3] = price
        all_balances[i][4] = "CURRENCY"
        i += 1
    return all_balances

def get_price():
    return poloniex.get_price("ETH")
