from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, status
from fastapi.responses import JSONResponse
import redis

# import bcrypt
import os
import jwt
from pathlib import Path

# db_token = int(os.environ.get("REDIS_TOKEN_DB"))
# db_user_access = int(os.environ.get("REDIS_USER_ACCESS_DB"))
# db_user_access = int(os.environ.get("REDIS_USER_ACCESS_DB"))

r = redis.Redis(host="localhost", port=6379, db=10)
r2 = redis.Redis(host="localhost", port=6379, db=11)


class RedisType:
    TOKEN = r
    USER_ACCESS = r2


class ValidatePermission(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        path = request.url.path
        pathExclude = [
            "/login",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/favicon.ico",
        ]

        # if path in pathExclude:
        #    return response

        for pe in pathExclude:
            if path.find(pe) > -1:
                return response

            elif "static" in path:
                return response

        token = request.headers.get("token")
        if token is None:
            return JSONResponse(
                {
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "message": "must provided by token",
                }
            )

        granted = getDataInRedis(token, RedisType.TOKEN)
        if not granted:
            return JSONResponse(
                {
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "message": "you dont have access to this data",
                }
            )
        else:
            return response


def setDataInRedis(key, value, type):
    load_dotenv(".env")
    exp = int(os.environ.get("REDIS_EXP"))

    if type == RedisType.TOKEN:
        r.set(key, value, ex=exp)
    else:
        r2.set(key, value, ex=exp)


def getDataInRedis(key, type):
    try:
        if type == RedisType.TOKEN:
            r.get(key).decode("utf-8")
            token = dict(decode_token(key))
            return token

        else:
            user_id = r2.get(key).decode("utf-8")
            user_access = decode_user_access(user_id)
            return user_access

    except:
        return False


def decode_token(token):
    try:
        payload = jwt.decode(token, "SECRET", algorithms=["HS256"])
        return {
            "user_id": payload["user_id"],
            "client_id": payload["client_id"],
            "username": payload["username"],
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail="Invalid token")


def decode_user_access(user_access):
    try:
        payload = jwt.decode(user_access, "SECRET", algorithms=["HS256"])
        return {"user_access": payload["user_access"]}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail="Invalid token")
