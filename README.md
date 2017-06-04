# CCAS - CryptoCurrency Accounting System

CCAS is a program to automate checking balances on many wallets and exchanges. It supports checking prices and counting summary balances in BTC and USD.

## First run

- Install required packages:
```
pip install Flask
pip install pycryptodome
```
- Run `runserver.py`
- Open browser default on http://localhost:5000/

## Optional parameters for `runserver.py`
```
  -h, --help            help
  -H HOST, --host=HOST  Hostname/IP of CCAS [default localhost]
  -P PORT, --port=PORT  Port for the CCAS [default 5000]
```


## To do: 
- [ ] Set interval between checking data
- [ ] Reset database to default
- [ ] Add history


## Supported exchanges:
- [X] Poloniex
- [X] BTC-e
- [X] Bittrex
- [X] Bitfinex


## Supported currency:
- [X] BTC
- [X] ETH
- [X] LTC
- [X] ERC20
