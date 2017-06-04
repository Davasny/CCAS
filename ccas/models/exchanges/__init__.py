from . import poloniex, btc_e, bittrex, bitfinex
from ccas.models import database, coinmarketcap


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
    exchange = database.new_query("SELECT `exchange` FROM `coins_prices` WHERE `name`='btc';")
    if exchange:
        exchange = exchange[0][0]
        if exchange == "poloniex":
            return poloniex.get_btc_price()
        if exchange == "btc-e":
            return btc_e.get_btc_price()
        if exchange == "bittrex":
            return bittrex.get_btc_price()
        if exchange == "bitfinex":
            return bitfinex.get_btc_price()
    else:
        return -1


def get_price(currency):
    exchange = database.new_query("SELECT `exchange` FROM `coins_prices` WHERE `name`='"+ currency.lower() +"';")
    if exchange:
        exchange = exchange[0][0]
        if exchange == "poloniex":
            return poloniex.get_price(currency)
        if exchange == "btc-e":
            return btc_e.get_price(currency)
        if exchange == "bittrex":
            return bittrex.get_price(currency)
        if exchange == "bitfinex":
            return bitfinex.get_price(currency)
        if exchange == "coinmarketcap":
            return coinmarketcap.get_price(currency)
    else:
        return -1
