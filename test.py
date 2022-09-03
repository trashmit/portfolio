import re

def password_strong(password):
    if len(password) < 8:
        return {"message":"Password too short"}
    digit = re.search(r"\d", password) #if there is no digit digit_error will be None
    uppercase = re.search(r"[A-Z]", password)   
    lowercase = re.search(r"[a-z]", password)
    symbol = re.search(r"\W", password)
    if digit or uppercase or lowercase or symbol: #if any error raise error
        return {"message":"success"}
    return {"message":"Password not strong enough!"}

print(password_strong("testing@"))