import urllib
import urllib.request
import json

def get_balance(list_of_address):
    string_of_addresses = ''
    for address in list_of_address:
        string_of_addresses = string_of_addresses + '|' + address

    raw_json = urllib.request.urlopen(
        'https://blockchain.info/pl/balance?active=' + string_of_addresses)
    parsed = json.loads(raw_json.read().decode('utf=8'))

    final_balances = {}
    for address in parsed:
        final_balances[address] = parsed['final_balance'] / (10**8)

    return final_balances
