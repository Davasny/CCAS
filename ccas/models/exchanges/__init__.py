from . import poloniex


def get_balances(exchange):
    if exchange == "poloniex":
        return poloniex.get_balances()
