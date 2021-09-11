import time
from config.settings import HASURA_SECRET_KEY
from jose import jwt

ALGORITHM = "HS256"

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, HASURA_SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except:
        return {}