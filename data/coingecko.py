import aiohttp
import asyncio
import time
import requests

class Coingecko:
    def __init__(self) -> None:
        self.tickers = self.updatecoins()
    
    async def get_image(self, ticker) -> str:
        async with aiohttp.ClientSession() as session:
            try:
                id = self.tickers[ticker.lower()] #gets the ID of the ticker
            except KeyError:#can't find ticker
                return "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/emojipedia/132/mage_1f9d9.png"
            data = await session.get(f"https://api.coingecko.com/api/v3/coins/{id}")
            info = await data.json()
            return info["image"]["small"] #returns url of image
            
            
    def updatecoins(self) -> dict: 
        response = requests.get(f"https://api.coingecko.com/api/v3/coins/list")
        data =  response.json()
        tickers = {}
        for dictionary in data:
            symbol = dictionary["symbol"] #gets a copy of its ticker
            tickers[symbol] = dictionary["id"] #{"ticker":"id"}
        return tickers

    async def get_total_marketcap(self) -> int:
        async with aiohttp.ClientSession() as session:
            response = await session.get("https://api.coingecko.com/api/v3/global")
            data = await response.json()
            return int(data["data"]["total_market_cap"]["usd"])