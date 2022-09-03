from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from web3.auto import w3
from fastapi.responses import HTMLResponse
from eth_account.messages import defunct_hash_message
import json
import time
import asyncio
import random
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt, ExpiredSignatureError
import re
import hashlib
templates = Jinja2Templates(directory="app")
import datetime
import asyncpg
from misc import Misc
Misc = Misc()
from consts import Consts
Consts = Consts()
from datetime import timedelta, datetime

SECRET = "0249524a254a329d8366ffcdb03b25e4eecb5da6986228ebabbd9e59f69dce3c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 60*60*24*7
SALT = "e4eecb5da69"

router = APIRouter(
    prefix="/api/users",
    tags = ["users"]
)

async def generate_nonce():
    return random.randint(99999, 1000001)

@router.on_event("startup")
async def startup_event():
    global conn
    conn = await asyncpg.connect(Consts.dbname)

async def generate_jwt(data):
    expire = time.time() + ACCESS_TOKEN_EXPIRE_SECONDS
    data["exp"] = expire
    print(data)
    return jwt.encode(data, SECRET, algorithm=ALGORITHM)

async def decode_jwt(token):
    print("DECODING")
    try:
        data = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return data
    except ExpiredSignatureError:
        return "expired"
    except JWTError:
        return "invalid"

@router.get("/getnonce/")
async def get_nonce(address):
    row = await conn.fetchrow('SELECT * FROM ethauth WHERE id = $1', address)
    print(row)
    if row:
        return {"message":row["nonce"]}
    else:
        a = await create_user(address)
        return a

@router.get("/check/")
async def return_cookies(_request : Request):
    return await Misc.verify_cookies(_request.cookies)
 

@router.post("/verifysignature/")
async def verify_signature(address, signature):
    nonce = await get_nonce(address)
    print(f"verifying with: {nonce['message']}")
    s = defunct_hash_message(text=f"verifying with: {nonce['message']}")
    if str(w3.eth.account.recoverHash(s, signature=signature)).lower() == address.lower():
        #content = {"message":"success"}
        #response = JSONResponse(content=content)
        content = {"message":"success", "data":{"cookie":await generate_jwt({"address":address.lower()}), "expires":str( (datetime.now() + timedelta(7)).strftime('%Y-%m-%d') )}}

        #creates cookie and stores it in user's cookie data, expires in 
        #response.set_cookie(key="access_token", value=await generate_jwt({"address":address.lower()}), domain="127.0.0.1", expires=60*60*24*7)
        return content
    else:
        return {"message":"fail"}

async def create_user(username:str):
    #Checks for a user with the same username in the database
    row = await conn.fetchrow('SELECT * FROM ethauth WHERE id = $1', username)
    print(row)
    if row: 
        return {"message":"username taken"}
    nonce = await generate_nonce()
    await conn.execute('''INSERT INTO ethauth (id, nonce) VALUES ($1, $2)''', username, nonce)
    await conn.execute('''INSERT INTO keys (id, key) VALUES ($1, $2)''', username, json.dumps({"btc":[], "ftx":[], "eth":[username]}))
    #inserts username and nonce into database
    return {"message":str(nonce)}


def password_strong(password):
    if len(password) < 8:
        return {"message":"Password too short"}
    digit = re.search(r"\d", password) #if there is no digit digit_error will be None
    uppercase = re.search(r"[A-Z]", password)   
    lowercase = re.search(r"[a-z]", password)
    symbol = re.search(r"\W", password)
    if digit and uppercase and lowercase and symbol: #if any error raise error
        return {"message":"success"}
    return {"message":"Password not strong enough!"}
    
def hash_and_salt(data):
    data = data + SALT #appends salt to whatever needs to be hashed
    m = hashlib.sha256() #gets ready to hash
    m.update(bytes(data, encoding="utf-8")) #hashes
    return m.hexdigest()  #returns hash in hex

@router.post("/signup/")
async def sign_up (username, password):
    if w3.isAddress(username):
        return {"message":"error"}
    if password_strong(password)["message"] == "success":
        username, password = hash_and_salt(username), hash_and_salt(password) #hashes the username and password
        row = await conn.fetchrow('SELECT * FROM normalauth WHERE id = $1', username) #finds a row with the username
        if row: #if the row exists
            return {"message":"Username is already taken!"}
        else:
            await conn.execute('''INSERT INTO normalauth (id, password) VALUES ($1, $2)''', username, password)
            await conn.execute('''INSERT INTO keys (id, key) VALUES ($1, $2)''', username, json.dumps({"btc":[], "ftx":[], "eth":[]}))
            return {"message":"success", "data":{"cookie":await generate_jwt({"address":username.lower()}), "expires":str( (datetime.now() + timedelta(7)).strftime('%Y-%m-%d') )}}
    return {"message":"Password not strong enough!"}

@router.post("/signin/")
async def sign_in (username, password):
    print(username, password)
    username, password = hash_and_salt(username), hash_and_salt(password) #hashes the username and password
    row = await conn.fetchrow('SELECT * FROM normalauth WHERE id = $1', username) #finds a row with the username
    if row:
        if row["password"] == password: #if passwords match
            return {"message":"success", "data":{"cookie":await generate_jwt({"address":username.lower()}), "expires":str( (datetime.now() + timedelta(7)).strftime('%Y-%m-%d') )}}
        else: # if passwords don't match
            return {"message":"fail"}
    return {"message":"fail"} #if username isn't found

