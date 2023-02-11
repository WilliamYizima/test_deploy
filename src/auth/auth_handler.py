import os
import time
from typing import Dict
import uuid
import jwt


JWT_SECRET = os.environ.get("SECRET_JWT", str(uuid.uuid4()))
JWT_ALGORITHM = "HS256"

def token_response(token: str):
    return {
        "access_token": token,
        "refresh": int(os.environ.get("JWT_EXPIRES")),
    }


def signJWT(user_id: str) -> Dict[str, str]:

    payload = {"user_id": user_id, "expires": time.time() + int(os.environ.get("JWT_EXPIRES"))}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
