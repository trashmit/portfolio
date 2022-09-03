from fastapi import APIRouter, Request
import asyncpg, json
from misc import Misc
Misc = Misc()
from consts import Consts
Consts = Consts()
from data.btc import Btc
Btc = Btc()
from data.ftx import Ftx
Ftx = Ftx()


NETWORKS = ["ftx", "btc", "eth"]

router = APIRouter(
                    prefix="/api/keys",
                    tags=["keys"]
                    )

@router.on_event("startup")
async def startup_event():
    global conn
    conn = await asyncpg.connect(Consts.dbname)


@router.post("/addkey/")
async def add_key(_request: Request, network, api_key):
    network = network.lower()
    print(api_key)
    print(type(api_key))
    if network == "ftx":
        api_key = l_x = [i.strip() for i in api_key[1:-1].replace('"',"").split(',')]
        print(type(api_key))
    auth = await Misc.verify_cookies(_request.cookies)
    if auth["status"] == "fail":
        return auth
    username = auth["message"] #gets ^ username from cookies if authenticated
    row = await conn.fetchrow('SELECT * FROM keys WHERE id = $1', username)
    if row is None:
        return {"message":"user not found"}
    if network in NETWORKS:
        data = (json.loads(row["key"])) #gets dictionary of exchange keys/ addresses
        if await key_valid(network, api_key) == False: #if the key is invalid
            return {"message":"invalid key"}
        if network in data.keys(): #checks if network is already a part of the dictionary
            data[network].append(api_key)
        else:
            data[network] = [api_key] #creates new keypair and puts list as value
        await conn.execute("UPDATE keys SET key = $1 WHERE id = $2;", json.dumps(data), username)
        return {"message":"success"}
    else:
        return {"message":"error"}

@router.post("/removekey/")
async def remove_key(_request: Request, network:str, api_key:str):
    network = network.lower()
    api_key=api_key.lower()
    auth = await Misc.verify_cookies(_request.cookies)
    if auth["status"] == "fail":
        return auth
    username = auth["message"] #gets ^ username from cookies if authenticated
    row = await conn.fetchrow('SELECT * FROM keys WHERE id = $1', username)
    if row is None:
        return {"message":"user not found"}
    if network in NETWORKS: #if network is valid
        data = (json.loads(row["key"])) #parses the keys stored in db
        if network in data.keys(): #checks if key exists in dictionary to avoid key error
            if api_key in data[network]: #if key is exists
                data[network].remove(api_key)
                await conn.execute("UPDATE keys SET key = $1 WHERE id = $2;", json.dumps(data), username) #update key
                return {"message":"success"}
            else:
                return {"message":"key not found"}
        return {"message":"key not found"}
    else:
        return {"message":"network not found"}

@router.get("/getkeys/")
async def add_key(_request: Request):
    username = await Misc.verify_cookies(_request.cookies)
    row = await conn.fetchrow('SELECT * FROM keys WHERE id = $1', username)
    data = (json.loads(row["key"]))
    try:
        data["ftx"] = "*"*25
    except:
        pass
    return data


async def key_valid(type, key):
    type = type.lower()
    if type in NETWORKS:
        if type == "ftx":
            return await Ftx.verify_key(key)
        elif type == "btc":
            if len(key) > 10:
                return True
            else:
                return False
    else:
        return False