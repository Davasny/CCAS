from ccas.models import database
from . import btc, eth, ltc

def get_details(curerncy, list_of_addresses, type):
    if curerncy == "BTC" and type == "balance":
        return btc.get_balance(list_of_addresses)
    elif curerncy == "ETH" and type == "balance":
        return eth.get_balance(list_of_addresses)
    elif curerncy == "LTC" and type == "balance":
        return ltc.get_balance(list_of_addresses)


def get_all_wallets(*args):
    if args:
        response = database.new_query("SELECT id, currency, name, address FROM wallets WHERE currency='"+ args[0] +"' ;")
    else:
        response = database.new_query("SELECT id, currency, name, address FROM wallets;")
    return list(response)


def get_wallets(currency):
    response = database.new_query("SELECT id, exchange FROM wallets WHERE currency;")
    return list(response)
