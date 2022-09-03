import requests, psycopg2, time, datetime
from consts import Consts
from data.ftx import Ftx
Ftx = Ftx()
import asyncio

Consts = Consts()
ADMINPASSWORD = "ADMinisduyfhas78dfyaso8df"
conn = psycopg2.connect(Consts.dbname)
cursor = conn.cursor()

async def historical():
    iterrr = 1
    while True:
        #adds eth price to historical
        cursor.execute("SELECT * FROM keys WHERE id = 'eth'")
        eth = cursor.fetchall()[0]
        eth[2].append(await Ftx.get_price("ETH_USD"))
        cursor.execute("UPDATE keys SET historical = %s WHERE id = %s;", (eth[2], eth[0]))
        conn.commit()
        #adds btc price to historical
        cursor.execute("SELECT * FROM keys WHERE id = 'btc'")
        btc = cursor.fetchall()[0]
        btc[2].append(await Ftx.get_price("BTC_USD"))
        cursor.execute("UPDATE keys SET historical = %s WHERE id = %s;", (btc[2], btc[0]))
        conn.commit()
        #adds users portfolio value to database
        cursor.execute("SELECT * FROM keys;")#gets all the data in DB
        users = cursor.fetchall() 
        for user in users:
            if user[0] == "btc" or user[0] == "eth":
                pass
            else:
                #user = (id, keys, historical)
                cookies = {"admin":ADMINPASSWORD, "username":"0xd2b101d3a69b20ac140ce233a67dd88abb0222b1"} #creates admin cookies
                data = requests.get(f"{Consts.domain_name}/api/portfolio/balances", cookies=cookies)
                #print(data.text)
                data = data.json()  #
                if type(user[2]) == list: #if the field isn't empty // has data in it
                    user[2].append([data["message"]["total"], datetime.datetime.now().strftime("%H:%M:%S %B %d, %Y") ]) 
                cursor.execute("UPDATE keys SET historical = %s WHERE id = %s;", (user[2], user[0]))
                conn.commit()
        print(iterrr)
        iterrr = iterrr + 1
        time.sleep(30) #hour

loop=asyncio.get_event_loop().run_until_complete(historical())

    
    
        

