
import aiohttp
import asyncio
import json
import time
import coinaddr

class Btc:
    def __init__(self) -> None:
        self.base_url = "https://blockchain.info/"
        self.digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        #loop = asyncio.get_event_loop()
        #print(loop.run_until_complete(self.verify_key("bc1qyylelu397yd946zvyg8z7lchwwurc7kyv9ng3v")))
    
    async def get_btc_price(self):
        async with aiohttp.ClientSession() as session:
            r = await session.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
            data = await r.json()
            return float(data["bitcoin"]["usd"])
    
    async def get_data(self, address):
        async with aiohttp.ClientSession() as session:
            r = await session.get(f"{self.base_url}rawaddr/{address}")
            if r.status == 429:
                return ['BTC',0,0]
            data = await r.json()
            current_balance = data["final_balance"]/100000000 # convert sats to btc
            price = await self.get_btc_price()
            return ['BTC', current_balance, price*current_balance, "https://assets.coingecko.com/coins/images/1/small/bitcoin.png"]
    
    async def get_btc_dated_price(self, timestamp) -> float:
        async with aiohttp.ClientSession() as session:
            r = await session.get(f"https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=USD&limit=1&toTs={timestamp}")
            data = await r.json()
            return data["Data"]["Data"][-1]["close"]

    async def get_all_transactions(self, address):
        """
        Returns list of a lists of transactions
        [Buy/Sell, Timestamp, BTC Value, BTC Price at time of tx]
        Sorted by timestamp so oldest transactions are first
        """
        async with aiohttp.ClientSession() as session:
            r = await session.get(f"{self.base_url}rawaddr/{address}?&n=100")
            print(r.status)
            data = await r.json()
            transactions = []
            for transaction in data["txs"]:
                price = await self.get_btc_dated_price(transaction["time"])
                for i in transaction["inputs"]:
                    #print(i)
                    #print(i.keys())
                    if i["prev_out"]["addr"] == address:
                        transactions.append(["out",transaction["time"], i["prev_out"]["value"]/100000000, price]) 
                for j in transaction["out"]:
                    if j["addr"] == address:
                        transactions.append(["in", transaction["time"], j["value"]/100000000, price])
            transactions.sort(key = lambda x: x[1])
            return transactions
        
    async def calculate_average_buy(self, address):
        """
        iterate through transactions
        If in Average Price = Total Amount Bought / Total Shares Bought
        If out subtract total btc bought
        """
        transactions = await self.get_all_transactions(address)
        total_usd_bought = 0
        average_price = 0
        total_btc_bought = 0
        for transaction in transactions:
            if transaction[0] == "in":
                total_btc_bought = total_btc_bought + transaction[2]
                total_usd_bought = total_usd_bought + transaction[2] * transaction[3]
                average_price = total_usd_bought/total_btc_bought
            elif transaction[0] == "out":
                total_btc_bought = total_btc_bought - transaction[2]
                total_usd_bought = total_usd_bought - transaction[2] * average_price
        print(f"{total_btc_bought} BTC at {average_price}$ average price")
 


    async def verify_key(self, key):
        return coinaddr.validate('btc', bytes(key, "UTF-8")).valid


#b = Btc()
