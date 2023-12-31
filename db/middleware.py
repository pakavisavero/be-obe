from fastapi import HTTPException
from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy import desc, asc

from db.models import *
from dotenv import load_dotenv
from datetime import datetime, timedelta
from datetime import datetime

import redis
import os
import jwt
import bcrypt

load_dotenv(".env")

db_token = int(os.environ.get("REDIS_TOKEN_DB"))
access_token = int(os.environ.get("REDIS_USER_ACCESS_DB"))

r = redis.Redis(host="localhost", port=6379, db=db_token)
r2 = redis.Redis(host="localhost", port=6379, db=access_token)


class RedisType:
    TOKEN = r
    USER_ACCESS = r2


class ValidatePermission(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        load_dotenv('.env')
        production = int(os.environ.get("PRODUCTION"))

        is_production = False
        if production == 0:
            is_production = False
        else:
            is_production = True

        path = request.url.path
        root = "be-obe"

        pathExclude = [
            "/login",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/favicon.ico",
            "/get-template",
            "/get-form-siap",
            "/get-portofolio",
            "/test-jinja",
            "/export"
        ]

        if is_production:
            pathExclude = [
                "/{}/login".format(root),
                "/{}/docs".format(root),
                "/{}/redoc".format(root),
                "/{}/openapi.json".format(root),
                "/{}/get-template".format(root),
                "/{}/get-form-siap".format(root),
                "/{}/get-portofolio".format(root),
                "/{}/test-jinja".format(root),
            ]

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


def authLogin(db: Session, email: str, password: str, role_id: int = 0):
    try:
        bytes = password.encode("utf-8")
        user = db.query(User).filter_by(email=email).first()

        if user:
            res = bcrypt.checkpw(bytes, user.password)
            user.last_login = datetime.now()
            db.commit()

            if res:
                if not user.is_active:
                    return {
                        "code": status.HTTP_404_NOT_FOUND,
                        "message": "User Not Active",
                    }

                u_access = get_user_access(db, user.id, role_id)
                groups = get_list_groups(db, user.id, role_id)

                if 'type' in u_access:
                    return {
                        "multi": True,
                        "code": status.HTTP_200_OK,
                        "message": "Succes get multi role!",
                        "data": u_access['data']
                    }

                token = encode_token(db, user.id, role_id)
                encode_u_access = encode_user_access(u_access)
                encode_group = encode_groups(groups)

                setDataInRedis(token, user.id, RedisType.TOKEN)
                setDataInRedis(user.id, encode_u_access, RedisType.USER_ACCESS)

                return {
                    "code": status.HTTP_200_OK,
                    "message": "Succes get token",
                    "token": token,
                    "user_access": encode_u_access,
                    "groups": encode_group,
                }
            else:
                return {
                    "code": status.HTTP_404_NOT_FOUND,
                    "message": "invalid password",
                }

        return {
            "code": status.HTTP_404_NOT_FOUND,
            "message": "User Not Found",
        }

    except Exception as e:
        print("ERROR", e)
        return False


def authLogout(token: str, db: Session):
    try:
        tokenDecode = decode_token(token)
        user = db.query(User).filter_by(id=tokenDecode["user_id"]).first()
        if user:
            r.delete(token)
            r2.delete(tokenDecode["user_id"])
            return {
                "code": status.HTTP_200_OK,
                "message": "Success Logout",
            }
        else:
            return {
                "code": status.HTTP_404_NOT_FOUND,
                "message": "User Not Found",
            }

    except Exception as e:
        print("ERROR", e)
        return False


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


def get_list_groups(db, user_id, role_id):
    role = ''

    if role_id != 0:
        role = db.query(UserRole).filter_by(
            user_id=user_id, role_id=role_id).first()
    else:
        role = db.query(UserRole).filter_by(user_id=user_id).first()

    access = db.query(RolePermission).filter_by(
        role_id=role.role_id).order_by(asc(RolePermission.module_id)).all()

    groups = []
    for u in access:
        if u.view:
            id = u.module.moduleGroup.id
            groupName = u.module.moduleGroup.module_name
            if len(groups) > 0:
                isExist = False
                for i, _ in enumerate(groups):
                    if groups[i]["group"] == groupName:
                        groups[i]["modules"].append(
                            {"name": u.module.module_name, "path": u.module.path}
                        )
                        isExist = True

                if not isExist:
                    arr = [{"name": u.module.module_name, "path": u.module.path}]
                    groups.append(
                        {
                            "group": groupName,
                            "modules": arr,
                            "icon": u.module.moduleGroup.icon,
                            "path": u.module.moduleGroup.path,
                        }
                    )

            else:
                arr = [{"name": u.module.module_name}]
                groups.append(
                    {
                        "group": groupName,
                        "modules": arr,
                        "icon": u.module.moduleGroup.icon,
                        "path": u.module.moduleGroup.path,
                    }
                )

    return groups


def get_user_access(db, user_id, role_id):
    role = ""
    if role_id != 0:
        role = db.query(UserRole).filter_by(
            user_id=user_id, role_id=role_id).all()
    else:
        role = db.query(UserRole).filter_by(user_id=user_id).all()

    if len(role) > 1:
        roles = []
        for r in role:
            roles.append({
                "id": r.roleMaster.id,
                "role_name": r.roleMaster.role_name,
            })

        return {
            'type': 'MULTI',
            'data': roles
        }

    access = db.query(RolePermission).filter_by(role_id=role[0].role_id).all()
    user_access = []

    for u in access:
        temp = (
            {
                "module_id": u.module_id,
                "module_name": u.module.module_name,
                "access": [
                    {
                        "view": u.view,
                        "add": u.add,
                        "edit": u.edit,
                        "print": u.printt,
                        "export": u.export,
                    }
                ],
            },
        )

        user_access.append(temp)

    return user_access


def encode_groups(groups):
    exp = int(os.environ.get("JWT_EXP"))
    payload = {
        "exp": datetime.utcnow() + timedelta(minutes=exp),
        "iat": datetime.utcnow(),
        "groups": groups,
    }

    return jwt.encode(payload, "SECRET", algorithm="HS256")


def encode_user_access(user_access):
    exp = int(os.environ.get("JWT_EXP"))
    payload = {
        "exp": datetime.utcnow() + timedelta(minutes=exp),
        "iat": datetime.utcnow(),
        "user_access": user_access,
    }

    return jwt.encode(payload, "SECRET", algorithm="HS256")


def encode_token(db, user_id, role_id):
    exp = int(os.environ.get("JWT_EXP"))

    dataUser = db.query(User).filter_by(id=user_id).first()
    roleName = ''
    if role_id != 0:
        roleName = db.query(UserRole).filter_by(
            user_id=user_id, role_id=role_id).first()
    else:
        roleName = db.query(UserRole).filter_by(user_id=user_id).first()

    payload = {
        "exp": datetime.utcnow() + timedelta(minutes=exp),
        "iat": datetime.utcnow(),
        "user_id": user_id,
        "nip": dataUser.nip,
        "email": dataUser.email,
        "fullName": dataUser.full_name,
        "role": roleName.roleMaster.role_name,
        "role_id": roleName.roleMaster.id,
        "username": dataUser.username,
        "prodi": dataUser.prodi.prodi,
        "lastLogin": datetime.strftime(dataUser.last_login, "%m/%d/%Y, %H:%M:%S"),
    }

    return jwt.encode(payload, "SECRET", algorithm="HS256")


def decode_token(token, all=False):
    try:
        payload = jwt.decode(token, "SECRET", algorithms=["HS256"])
        if all:
            return payload

        return {
            "user_id": payload["user_id"],
            "email": payload["email"],
            "nip": payload['nip'],
            "username": payload["username"],
            "fullName": payload["fullName"],
            "role": payload["role"],
            "prodi": payload["prodi"],
            "lastLogin": payload["lastLogin"],
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


def decode_group(group):
    try:
        payload = jwt.decode(group, "SECRET", algorithms=["HS256"])
        return {"group": payload["groups"]}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail="Invalid token")
