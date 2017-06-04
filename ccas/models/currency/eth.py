import urllib
import urllib.request
import json
from decimal import *
from ccas.models import exchanges


def get_balance(list_of_address):
    return_reposne = {}
    #try:
    if isinstance(list_of_address[0], list):
        use_names = True
    else:
        use_names = False

    all_balances = []

    for address in list_of_address:
        tmp_balances = []

        raw_json = urllib.request.urlopen(
            'https://api.ethplorer.io/getAddressInfo/' + address[0] + '?apiKey=freekey')
        parsed = json.loads(raw_json.read().decode('utf-8'))

        price = exchanges.get_price("ETH")

        tmp_balances.append("ETH")
        tmp_balances.append(parsed['address'])
        tmp_balances.append(Decimal(parsed['ETH']['balance']) / (10**18))
        tmp_balances.append(price)
        tmp_balances.append("CURRENCY")

        if use_names:
            tmp_balances.append(address[1])
        else:
            tmp_balances.append('')


        all_balances.append(tmp_balances)
        tmp_balances = []
        if 'tokens' in parsed:
            for token_data in parsed['tokens']:
                price = exchanges.get_price(token_data['tokenInfo']['symbol'])

                tmp_balances.append(token_data['tokenInfo']['symbol'])
                tmp_balances.append(parsed['address'])
                tmp_balances.append(Decimal(token_data['balance']) / (10 ** Decimal(token_data['tokenInfo']['decimals'])))
                tmp_balances.append(price)
                tmp_balances.append("CURRENCY-ETH_TOKEN")

                if use_names:
                    tmp_balances.append(address[1])
                else:
                    tmp_balances.append('')

                all_balances.append(tmp_balances)


    return_reposne["status"] = True
    return_reposne["data"] = all_balances


    #except Exception as e:
    #    return_reposne["status"] = False
    #    return_reposne["msg"] = e

    return return_reposne
