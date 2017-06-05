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


def get_coin_prices_settings():
    response = database.new_query("SELECT `id`, `name`, `exchange` FROM coins_prices;")
    return list(response)


def update_coin_prices_settings(coin, new_exchange):
    if_exist = database.new_query("SELECT count(1) FROM `coins_prices` WHERE `name`='"+ coin +"'")[0][0]
    if if_exist:
        response = database.new_argument_query("UPDATE `coins_prices` SET `exchange`=? WHERE `name`=?",
                                               (new_exchange, coin))
    else:
        response = database.new_argument_query("INSERT INTO `coins_prices` (`exchange`, `name`) VALUES (?, ?)",
                                               (new_exchange, coin))
    return response
