import aiohttp
import asyncio
import json
import time
import hmac
from data.coingecko import Coingecko
Coingecko = Coingecko()

class Ftx:
    def __init__(self) -> None:
        self.base_url = "https://ftx.com/api/"

    async def build_headers(self, path, api, secret):
        ts = int(time.time() * 1000)
        signature = hmac.new(secret.encode(), f'{ts}GET/api/{path}'.encode(), 'sha256').hexdigest()
        return {'FTX-KEY': api, "FTX-SIGN":signature, "FTX-TS":str(ts)}

    async def get_balances(self, api, secret):
        async with aiohttp.ClientSession() as session:
            headers = await self.build_headers("wallet/balances", api, secret)
            response = await session.get(f"{self.base_url}wallet/balances", headers=headers)
            data = await response.json()
            balances = []
            #print(data)
            for coin in data["result"]:
                if coin["usdValue"] > 0.1:
                    balances.append( [coin["coin"],coin["total"], coin["usdValue"], await Coingecko.get_image(coin["coin"]) ])
            return balances
    
    async def get_all_coins(self) -> list:     
        async with aiohttp.ClientSession() as session:
            response = await session.get(self.base_url + "/markets")
            data = await response.json()
            #print(data)
            coins = data["result"]
            symbols = []
            for coin in coins:
                symbols.append(coin["name"])
            return symbols

    async def get_coin_candles(self, market_name, timeframe) -> dict:
        async with aiohttp.ClientSession() as session:
            response = await session.get(f"{self.base_url}/markets/{market_name}/candles?resolution={timeframe}&limit={100}&start_time={time.time()-timeframe*100}")
            data = await response.json()
            #print(data)
            return data["result"]
        
    async def get_price(self, market) -> int:     
        async with aiohttp.ClientSession() as session:
            response = await session.get(self.base_url + f"/markets/{market}")
            data = await response.json()
            return data["result"]["price"]

    async def get_closes(self, market_name, timeframe) -> list:
        data = await self.get_coin_candles(market_name, timeframe)
        #print(data)
        closes = []
        for d in data:
            closes.append(d["close"])
        return closes
    
    async def verify_key(self, key):
        api, secret = key[0], key[1]
        async with aiohttp.ClientSession() as session:
            headers = await self.build_headers("wallet/balances", api, secret)
            response = await session.get(f"{self.base_url}wallet/balances", headers=headers)
            data = await response.json()
            print(data)
            if data["success"] == True:
                return True
            else:
                return False


#Ftx()
