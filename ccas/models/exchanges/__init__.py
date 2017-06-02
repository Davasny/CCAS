from . import poloniex, btc_e, bittrex, bitfinex
from ccas.models import database

def get_balances(exchange, public_key, secret_key):
    if exchange == "poloniex":
        return poloniex.get_balances(public_key, secret_key)
    if exchange == "btc-e":
        return btc_e.get_balances(public_key, secret_key)
    if exchange == "bittrex":
        return bittrex.get_balances(public_key, secret_key)
    if exchange == "bitfinex":
        return bitfinex.get_balances(public_key, secret_key)

def get_exchanges():
    response = database.new_query("SELECT id, exchange FROM exchanges_api_keys;")
    return list(response)

def get_btc_price():
    exchange = database.new_query("SELECT value FROM settings WHERE name='exchange_price_btc';")
    if exchange[0][0] == "btc-e":
        btc_price = btc_e.get_btc_price()
    return round(btc_price,2)


def get_price(currency):
    exchange = database.new_query("SELECT `value` FROM `settings` WHERE `name`='exchange_price_"+ currency.lower() +"';")[0][0]
    if exchange == "poloniex":
        return poloniex.get_price(currency)
    if exchange == "btc-e":
        return btc_e.get_price(currency)
    if exchange == "bittrex":
        return bittrex.get_price(currency)
    if exchange == "bitfinex":
        return bitfinex.get_price(currency)
    return 0
