import aiohttp
import asyncio
import json
import time
from misc import Misc
Misc = Misc()

class Binance:
    def __init__(self) -> None:
        self.BASE_URL = "https://api.binance.com/api/v3/"
        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(self.get_closes("BTCUSDT", "4h"))

    async def get_all_coins(self) -> list: #returns list of all tickers
        async with aiohttp.ClientSession() as session:
            response = await session.get(f"{self.BASE_URL}exchangeInfo")
            data = await response.json()
            symbols = []
            for s in data['symbols']:
                if "USD" in s['symbol']:
                    symbols.append(s['symbol'])
            return symbols
    
    async def get_coin_candles(self, market_name, timeframe) -> list:
        """ response #BINANCE GIVES MOST RECENT DATA LAST
            [
                [
                    1499040000000,      # Open time
                    "0.01634790",       # Open
                    "0.80000000",       # High
                    "0.01575800",       # Low
                    "0.01577100",       # Close
                    "148976.11427815",  # Volume
                    1499644799999,      # Close time
                    "2434.19055334",    # Quote asset volume
                    308,                # Number of trades
                    "1756.87402397",    # Taker buy base asset volume
                    "28.46694368",      # Taker buy quote asset volume
                    "17928899.62484339" # Can be ignored
                ]
            ]
        """
        timeframe = Misc.seconds_to_timeframe(timeframe)
        async with aiohttp.ClientSession(trust_env=True) as session:
            #print(f"{self.BASE_URL}klines?interval={timeframe}&limit=100&symbol={market_name}")
            response = await session.get(f"{self.BASE_URL}klines?interval={timeframe}&limit=100&symbol={market_name}") 
            data =await response.json() #still converts the response into a list
            return data

    async def get_closes(self, market_name, timeframe) -> list:
        data = await self.get_coin_candles(market_name, timeframe)
        closes = []
        for d in data:  
            #print(d)
            #print(type(d))
            closes.append(float(d[4]))
        closes.reverse()
        return closes

