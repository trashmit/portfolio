#for misc functions that aren't frontend specific
from jose import JWTError, jwt
import asyncio
import time

class Misc:
    def __init__(self) -> None:
        self._SECRET = "0249524a254a329d8366ffcdb03b25e4eecb5da6986228ebabbd9e59f69dce3c"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_SECONDS = 60*60*24*7
        self.SECRET = "ADMinisduyfhas78dfyaso8df"

    async def generate_jwt(self, data):
        expire = time.time() + self.ACCESS_TOKEN_EXPIRE_SECONDS
        data["exp"] = expire
        #print(data)
        return jwt.encode(data, self._SECRET, algorithm=self.ALGORITHM)

    async def decode_jwt(self, token):
        #print("DECODING")
        try:
            payload = jwt.decode(token, self._SECRET, algorithms=[self.ALGORITHM])
            return payload
        except JWTError:
            return False

    async def verify_cookies(self, cookies):
        #print(cookies)
        if cookies == {}:
            return {"status":"fail", "message":"You are not logged in!"}
        elif "admin" in cookies.keys(): #to avoid index error
            if cookies["admin"] == self.SECRET: 
                return {"status":"success", "message":cookies["username"]}
            else:
                return {"status":"fail", "message":"false admin password kys"}
        else:
            data = await self.decode_jwt(cookies["access_token"])
            #print(data)
            if data == "invalid":
                return {"status":"fail", "message":f"Your login cookie is invalid, login again!"}
            elif data == "expired":
                return {"status":"fail", "message":f"Your login cookie is expired, please login again!"}
            else:
                return {"status":"success", "message":data['address']}  

