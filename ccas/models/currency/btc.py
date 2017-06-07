import urllib
import urllib.request
import json
from decimal import *


def get_balance(list_of_address):
    return_reposne = {}
    try:
        string_of_addresses = ''
        address_name = {}

        if isinstance(list_of_address[0], list):
            use_names = True
            for element in list_of_address:
                address_name[element[0]] = element[1]
        else:
            use_names = False

        for address in list_of_address:
            if use_names:
                string_of_addresses = string_of_addresses + '|' + address[0]
            else:
                string_of_addresses = string_of_addresses + '|' + address


        raw_json = urllib.request.urlopen(
            'https://blockchain.info/en/balance?active=' + string_of_addresses)
        parsed = json.loads(raw_json.read().decode('utf-8'))

        all_balances = [([0] * 6) for i in range(len(parsed))]

        i = 0
        for address in parsed:
            all_balances[i][0] = "BTC"
            all_balances[i][1] = address
            all_balances[i][2] = Decimal(parsed[address]['final_balance'] / (10**8))
            all_balances[i][3] = 1
            all_balances[i][4] = "CURRENCY"

            if use_names:
                all_balances[i][5] = address_name[address]
            else:
                all_balances[i][5] = ''

            i += 1
        return_reposne["status"] = True
        return_reposne["data"] = all_balances

    except Exception as e:
        return_reposne["status"] = False
        return_reposne["msg"] = e

    return return_reposne
