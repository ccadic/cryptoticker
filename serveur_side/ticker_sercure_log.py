# (C) 2023 Dr CADIC Philippe @sulfuroid
# Socket serveur to connect to Binance via ccxt library
# get the crypto/USDT pair value
# Listens on port 1789
# Test it with: curl http://localhost:1789/BTC  do get BTC/USDT value
# Saves into a log file, please add full file path to "logging.basicConfig(filename='ticker.log', level=logging.INFO,"
# Please adapt ALLOWED_CRYPTOS = ['BTC', 'ETH', 'TRX', 'MATIC']  if you need more cryptos
# Instal the necessary libs: "pip install ccxt asyncio"

import ccxt
import asyncio
from aiohttp import web
import logging
from datetime import datetime

# Configuration de logging
logging.basicConfig(filename='/path/to_/ticker.log', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Initialisez l'objet binance
binance = ccxt.binance()

ALLOWED_CRYPTOS = ['BTC', 'ETH', 'TRX', 'MATIC']

async def get_price(request):
    client_ip = request.remote
    crypto = request.match_info.get('symbol').upper()

    # Log l'information
    logging.info(f"IP: {client_ip}, Crypto demandée: {crypto}")

    if crypto not in ALLOWED_CRYPTOS:
        return web.Response(text="Crypto non autorisée", status=400)

    try:
        symbol = crypto + "/USDT"
        ticker = binance.fetch_ticker(symbol)
        return web.Response(text=str(ticker['last']))
    except Exception as e:
        return web.Response(text=f"Erreur: {e}", status=400)

app = web.Application()
app.router.add_get('/{symbol}', get_price)

if __name__ == '__main__':
    web.run_app(app, port=1789)


'''How to run as a service on ubuntu 22.04

sudo nano /etc/systemd/system/ticker.service

#add this into ticker.service

[Unit]
Description=Ticker Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to_/script.py
Restart=always
User=nom_d_utilisateur
Group=groupe_d_utilisateur
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target

#Save 

# Then
sudo systemctl enable ticker.service
sudo systemctl start ticker.service
sudo touch /path/to_/ticker.log
sudo chown user:user /path/to_/ticker.log

sudo systemctl status ticker.service

'''
