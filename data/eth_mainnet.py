
import aiohttp
import asyncio
import json
import time
from construct import Float64b
from web3 import Web3
import json
import math
from data.ftx import Ftx
Ftx = Ftx()


# add your blockchain connection information





#d66824fe49d786b8875baa6746ad3b5c6b45445a8a9d6e978c7e204b5733de90

"""
Blockchain.info for address:
https://blockchain.info/rawaddr/$bitcoin_address
Address can be base58 or hash160


"""

class Eth:
    def __init__(self) -> None:
        self.base_url = "https://api.ethplorer.io/"
        self.headers = {'x-api-key': 'uSmjNOVNyvIm1NMZelXo2Bf9gDIKLkbyjRx1ogPLAFwUlsncYgO0BHQlPkKdL9Jb'}
        self._1inch = "https://api.1inch.exchange/v3.0/1"
        #loop = asyncio.get_event_loop()
        #print(loop.run_until_complete(self.get_balances("0xD2B101D3a69B20ac140ce233A67Dd88Abb0222B1")))

    async def get_balances(self, address) -> list:
        data = await self.get_data(address)
        #print(data)
        data = await self.get_prices(data)
        balances = []
        for balance in data:
            if balance["symbol"] == '':
                continue
            if balance["logo"]:
                url = balance["logo"]
            else:
                url = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/emojipedia/132/mage_1f9d9.png"
            value = float(balance['balance'])/ 10**int(balance["decimals"])
            balances.append([balance["symbol"], value, balance["usd"]*value, url])
        data = await self.get_eth_balance(address)
        balances.append(["eth", data, data* await Ftx.get_price("ETH_USD"), "https://assets.coingecko.com/coins/images/279/small/ethereum.png?1595348880"])
        return balances
        #print(balances)

    async def get_eth_balance(self, address) -> list:
        async with aiohttp.ClientSession() as session:
            headers = {'x-api-key': 'uSmjNOVNyvIm1NMZelXo2Bf9gDIKLkbyjRx1ogPLAFwUlsncYgO0BHQlPkKdL9Jb'}
            r = await session.get('https://deep-index.moralis.io/api/v2/'+ address + '/balance?chain=eth', headers=self.headers)
            resp = await r.json()
            return float(resp["balance"])/10**18

    async def get_data(self, address) -> list: #gets initial token data, eg users balances and tokens name
        async with aiohttp.ClientSession() as session:
            headers = {'x-api-key': 'uSmjNOVNyvIm1NMZelXo2Bf9gDIKLkbyjRx1ogPLAFwUlsncYgO0BHQlPkKdL9Jb'}
            r = await session.get('https://deep-index.moralis.io/api/v2/'+ address + '/erc20?chain=eth', headers=self.headers)
            resp = await r.json()
            return resp
    
    async def get_prices(self, balances):
        #{"message": "No pools found with enough liquidity, to calculate the price"}
        async with aiohttp.ClientSession() as session:
            for balance in balances:
                #print(balance)
                r = await session.get(f"https://deep-index.moralis.io/api/v2/erc20/{balance['token_address']}/price?chain=eth",headers = self.headers)
                resp = await r.json()
                #print(resp)
                if "message" in resp.keys():
                    balances.remove(balance)
                else:
                    balance["usd"] = resp["usdPrice"]
        return balances

eth = Eth()