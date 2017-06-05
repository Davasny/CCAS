# CCAS - CryptoCurrency Accounting System

CCAS is a program to automate checking balances on many wallets and exchanges. It supports checking prices and counting summary balances in BTC and USD.

## Installation
### Windows
1. Download ccas.zip from [Releases](https://github.com/Davasny/CCAS/releases/latest)
2. Unzip file
3. Run `ccas\runserver.exe`
6. Open browser default on [http://localhost:5000/](http://localhost:5000/)

### Linux
1. Install Python3.6
2. Install required packages:
```
pip install Flask
pip install pycryptodome
```
3. Download latest release code from [Releases](https://github.com/Davasny/CCAS/releases/latest)
4. Unzip code
5. Run `runserver.py`
6. Open browser default on [http://localhost:5000/](http://localhost:5000/)

## Optional parameters for `runserver.py`
```
  -h, --help            help
  -H HOST, --host=HOST  Hostname/IP of CCAS [default localhost]
  -P PORT, --port=PORT  Port for the CCAS [default 5000]
```


## To do: 
- [ ] Export and import settings


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


## Donations
You can appreciate my work on CCAS by sending me something for beer (I promise to spend most money on beer and show you that ;)
- BTC `1JdPUakQaMnKtXEsJqNBy78Efse7adSiPG`
- ETH `0xd5bde789E9Ce5fBf16e47600D5aDc845178efF8B`
- LTC `LU3Y3q3HAPjT5Q4pxym43XpZUWR68LHVpL`
