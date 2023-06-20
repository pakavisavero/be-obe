from fastapi import HTTPException
from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware

from db.models import *
from controller import user

from dotenv import load_dotenv
from datetime import datetime, timedelta
import redis
import os
import jwt
import bcrypt

load_dotenv(".env")

db_token = int(os.environ.get("REDIS_TOKEN_DB"))
access_token = int(os.environ.get("REDIS_USER_ACCESS_DB"))

r = redis.Redis(host="localhost", port=6379, db=1)
r2 = redis.Redis(host="localhost", port=6379, db=2)


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


# def authLogin(db: Session, email, password):
#     try:
#         bytes = password.encode("utf-8")
#         user = db.query(User).filter_by(email=email).first()

#         if user:
#             res = bcrypt.checkpw(bytes, user.password)
#             user.last_login = datetime.now()
#             db.commit()

#             if res:
#                 if not user.is_active:
#                     return {
#                         "code": status.HTTP_404_NOT_FOUND,
#                         "message": "User Not Active",
#                     }

#                 token = encode_token(db, user.id)
#                 u_access = get_user_access(db, user.id)
#                 encode_u_access = encode_user_access(u_access)
#                 setDataInRedis(token, user.id, RedisType.TOKEN)

#                 return {
#                     "code": status.HTTP_200_OK,
#                     "message": "Succes get token",
#                     "token": token,
#                     "user_access": encode_u_access,
#                 }
#             else:
#                 return {
#                     "code": status.HTTP_404_NOT_FOUND,
#                     "message": "invalid  password",
#                 }
#         return {
#             "code": status.HTTP_404_NOT_FOUND,
#             "message": "User Not Found",
#         }

#     except Exception as e:
#         print("ERROR", e)
#         return False


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


# def get_user_access(db, user_id):
#     role = db.query(RoleMaster).filter_by(user_id=user_id).first()
#     access = db.query(RolePermission).filter_by(role_id=role.id).first()

#     user_access = []
#     for u in access:
#         temp = (
#             {
#                 "module_id": u.module_id,
#                 "access": [
#                     {
#                         "view": u.view,
#                         "add": u.add,
#                         "edit": u.edit,
#                         "print": u.printt,
#                         "export": u.export,
#                     }
#                 ],
#             },
#         )

#         user_access.append(temp)

#     return user_access


# def encode_user_access(user_access):
#     exp = int(os.environ.get("JWT_EXP"))
#     payload = {
#         "exp": datetime.utcnow() + timedelta(minutes=exp),
#         "iat": datetime.utcnow(),
#         "user_access": user_access,
#     }

#     return jwt.encode(payload, "SECRET", algorithm="HS256")


# def encode_token(db, user_id):
#     exp = int(os.environ.get("JWT_EXP"))

#     dataUser = user.getByID(db, user_id)
#     roleName = db.query(UserRole).filter_by(user_id=user_id).first()

#     payload = {
#         "exp": datetime.utcnow() + timedelta(minutes=exp),
#         "iat": datetime.utcnow(),
#         "user_id": user_id,
#         "email": dataUser.email,
#         "fullName": dataUser.full_name,
#         "role_name": roleName.roleMaster.role_name,
#         "role_id": dataUser.roleMaster.id,
#     }

#     return jwt.encode(payload, "SECRET", algorithm="HS256")


def decode_token(token):
    try:
        payload = jwt.decode(token, "SECRET", algorithms=["HS256"])
        return {
            "user_id": payload["user_id"],
            "email": payload["email"],
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
