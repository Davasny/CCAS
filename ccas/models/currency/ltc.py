import urllib
import urllib.request
import json
from decimal import *
from ccas.models.exchanges import poloniex


def get_balance(list_of_address):
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

    all_balances = [([0] * 6) for i in range(len(parsed))]

    price = get_price()

    i = 0
    for account in parsed:
        all_balances[i][0] = "LTC"
        all_balances[i][1] = account['address']
        all_balances[i][2] = Decimal(account['balance'])
        all_balances[i][3] = price
        all_balances[i][4] = "CURRENCY"

        if use_names:
            all_balances[i][5] = list_of_address[i][1]
        else:
            all_balances[i][5] = ''

        i += 1

    return all_balances

def get_price():
    return poloniex.get_price("LTC")
