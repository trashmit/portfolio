import asyncio
import time, json
from fastapi import APIRouter, Request
import asyncpg
from misc import Misc
Misc = Misc()
from data.btc import Btc
Btc = Btc()
from data.ftx import Ftx
Ftx = Ftx()
from data.eth_mainnet import Eth
Eth = Eth()
from data.coingecko import Coingecko
Coingecko = Coingecko()
from consts import Consts
Consts = Consts()

router = APIRouter(
    prefix="/api/portfolio",
    tags = ["balances"]
)

@router.on_event("startup")
async def startup_event():
    global conn
    conn = await asyncpg.connect(Consts.dbname)

"""
@router.get("/balances/")
async def balances():

    data = await Misc.verify_cookies(_request.cookies)
    if data["status"] == "fail":
        return data
    username = data["message"] #gets username
    row = await conn.fetchrow('SELECT * FROM keys WHERE id = $1', username)
    keys = json.loads(row["key"])
    
    start = time.time()
    keys = {"btc": [], "ftx": [["MA7RJnazPavavIje5EFyr99lGpiPFXjWs-OHdVLY", "aUkECojqzsn08-IMm_WaoXn4oul6Wfv-Wrxpj-Y7"]], "eth": ["0xbb7003162386c494b09e9e0e874d1915426e70f7", "0xD2B101D3a69B20ac140ce233A67Dd88Abb0222B1"]}
    balances = []
    tasks = []
    if len(keys["btc"]) != 0:
        btcbalances = []
        for addy in keys["btc"]:
            tasks.append( Btc.get_data(addy))
    if len(keys["ftx"]) != 0:
        ftxcoins = []
        for key in keys["ftx"]:
            tasks.append( Ftx.get_balances(key[0], key[1]))
    if len(keys["eth"]) != 0:
        ethcoins=[]
        for addy in keys["eth"]:
            tasks.append(Eth.get_balances(addy))
    balances = asyncio.gather(*tasks)
    await balances
    print(balances)
    balances = [val for sublist in balances for val in sublist]
    print(balances)
    print(time.time()-start)
    #return {"message":{"total":(str(round(sum([item[2] for item in balances]), 2))), "portfolio":balances}}
"""


@router.get("/historical/")
async def get_historical_balance(username):
    conn = await asyncpg.connect(Consts.dbname)
    row = await conn.fetchrow('SELECT * FROM keys WHERE id = $1', username)
    #print(row)
    if row:
        return {"message":row[2]}
    return {"message":"user not found"}



@router.get("/balances/")
async def balances(_request: Request):
    validate = await Misc.verify_cookies(_request.cookies)
    #print(validate)
    row = await conn.fetchrow('SELECT * FROM keys WHERE id = $1', validate["message"])
    keys = json.loads(row["key"])
    #print(keys)
    a = time.time()
    balances = []
    if len(keys["btc"]) != 0:
        btcbalances = []
        for addy in keys["btc"]:
            btcbalances.append(await Btc.get_data(addy))
        #print(btcbalances)
        balances.append(["BTC", sum([item[1] for item in btcbalances]), sum([item[2] for item in btcbalances]), "https://assets.coingecko.com/coins/images/1/small/bitcoin.png"])
    if len(keys["ftx"]) != 0:
        ftxcoins = []
        for key in keys["ftx"]:
            ftxcoins.append(await Ftx.get_balances(key[0], key[1]))
        for coins in ftxcoins:
            for coin in coins:
                coin.append(await Coingecko.get_image(coin[0]))
                balances.append(coin)
    if len(keys["eth"]) != 0:
        ethcoins=[]
        for addy in keys["eth"]:
            ethcoins.append(await Eth.get_balances(addy))
        for coins in ethcoins:
            for coin in coins:
                balances.append(coin)
    #print({"message":{"total":(str(round(sum([item[2] for item in balances]), 2))), "portfolio":balances}})
    #print(a-time.time())
    return {"message":{"total":(str(round(sum([item[2] for item in balances]), 2))), "portfolio":balances}}


"""
@router.get("/balances/")
async def balances(_request: Request):
    data = await Misc.verify_cookies(_request.cookies)
    if data["status"] == "fail":
        return data
    username = data["message"] #gets username
    row = await conn.fetchrow('SELECT * FROM keys WHERE id = $1', username)
    keys = json.loads(row["key"])
    balances = []
    if len(keys["btc"]) != 0:
        btcbalances = []
        for addy in keys["btc"]:
            btcbalances.append(await Btc.get_data(addy))
        #print(btcbalances)
        balances.append(["BTC", sum([item[1] for item in btcbalances]), sum([item[2] for item in btcbalances]), "https://assets.coingecko.com/coins/images/1/small/bitcoin.png"])
    if len(keys["ftx"]) != 0:
        ftxcoins = []
        for key in keys["ftx"]:
            ftxcoins.append(await Ftx.get_balances(key[0], key[1]))
        for coins in ftxcoins:
            for coin in coins:
                coin.append(await Coingecko.get_image(coin[0]))
                balances.append(coin)
    if len(keys["eth"]) != 0:
        ethcoins=[]
        for addy in keys["eth"]:
            ethcoins.append(await Eth.get_balances(addy))
        for coins in ethcoins:
            for coin in coins:
                balances.append(coin)
    return {"message":{"total":(str(round(sum([item[2] for item in balances]), 2))), "portfolio":balances}}
"""