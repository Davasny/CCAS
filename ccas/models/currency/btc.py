import urllib
import urllib.request
import json
from decimal import *


def get_balance(list_of_address):
    string_of_addresses = ''
    for address in list_of_address:
        string_of_addresses = string_of_addresses + '|' + address

    raw_json = urllib.request.urlopen(
        'https://blockchain.info/pl/balance?active=' + string_of_addresses)
    parsed = json.loads(raw_json.read().decode('utf=8'))

    all_balances = [([0] * 5) for i in range(len(parsed))]

    i = 0
    for address in parsed:
        all_balances[i][0] = "BTC"
        all_balances[i][1] = address
        all_balances[i][2] = parsed[address]['final_balance'] / (10**8)
        all_balances[i][3] = 1
        all_balances[i][4] = "CURRENCY"
        i += 1

    return all_balances
