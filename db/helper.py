from fastapi import status
from db.middleware import getDataInRedis, RedisType
import pytz
from sqlalchemy import cast, String, Date, desc
from datetime import datetime, timedelta, date
from HandlerCustom import HandlerCustom
from sqlalchemy.orm import Session as tempSessionn
import os
import requests
import redis
import json
from dotenv import load_dotenv
from functools import wraps
import jwt
from enum import Enum


load_dotenv(".env")


r = redis.Redis(host="localhost", port=6379, db=5)
r2 = redis.Redis(host="localhost", port=6379, db=6)


class Microservices(Enum):
    USER = "SERVICE_USER"
    TRANSACTION = "SERVICE_TRANSACTION"


def helperGET(token: str, type: Microservices, segment: str, all=True, id: int = None):
    headersList = {"token": token}
    baseUrl = os.environ.get(type.value)
    url = baseUrl + segment

    if not all:
        url = baseUrl + segment + "/{}".format(id)

    response = requests.request("GET", url, headers=headersList)

    return json.loads(response.text)


def helperPOST(token: str, type: Microservices, segment: str, payload: dict):
    headersList = {"token": token}
    baseUrl = os.environ.get(type.value)
    url = baseUrl + segment

    response = requests.request("POST", url, payload=payload, headers=headersList)

    return json.loads(response.text)


def decode_token(token):
    granted = r.exists(token)
    if not granted:
        raise HandlerCustom(data={"message": "you dont have access to this data"})
    payload = jwt.decode(token, "SECRET", algorithms=["HS256"])
    return payload


def getCID(token):
    cid = decode_token(token)["client_id"]
    return cid


def changeBoll(name):
    if name == "true":
        return True
    return False


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


def is_foreign_key(column):
    return True if column.foreign_keys else False


def helper_static_filter(db, Schema, filtered, offset):
    page_size = 10
    dict_string = {}
    dict_number = {}
    dict_bool = {}
    dict_date = {}
    base_query = db.query(Schema)
    # if cid:
    #     base_query = base_query.filter_by(client_id=cid)
    for key in filtered:
        if key == "page_size":
            page_size = filtered[key]
        else:
            if isinstance(filtered[key], int):
                dict_number[key] = int(filtered[key])
            if isinstance(filtered[key], str):
                if str(filtered[key]) in ["true", "false"]:
                    dict_bool[key] = changeBoll(str(filtered[key]))
                else:
                    if "[" in str(key):
                        key_split = str(key).split("[")
                        index_key_spit = str(key_split[1]).split("]")[0]
                        if key_split[0] not in dict_date:
                            dict_date[key_split[0]] = [None, None]

                        dict_date[key_split[0]][int(index_key_spit)] = filtered[key]

                    else:
                        dict_string[key] = str(filtered[key])
    if dict_number:
        for key in dict_number:
            if dict_number[key] is not None:
                check = is_foreign_key(getattr(Schema, key))
                if check:
                    base_query = base_query.filter(
                        getattr(Schema, key) == dict_number[key]
                    )
                else:
                    base_query = base_query.filter(
                        cast(getattr(Schema, key), String).like(
                            "%{}%".format(dict_number[key])
                        )
                    )

    if dict_string:
        for key in dict_string:
            if dict_string[key]:
                base_query = base_query.filter(
                    getattr(Schema, key).ilike("%{}%".format(dict_string[key]))
                )

    if dict_date:
        for key in dict_date:
            start_date = datetime.strptime(
                dict_date[key][0][:10], "%Y-%m-%d"
            ).date() + timedelta(days=1)
            end_date = datetime.strptime(
                dict_date[key][1][:10], "%Y-%m-%d"
            ).date() + timedelta(days=1)

            if dict_date[key][0] == dict_date[key][1]:
                base_query = base_query.filter(
                    cast(getattr(Schema, key), Date) == start_date
                )
            else:
                base_query = base_query.filter(
                    cast(getattr(Schema, key), Date).between(start_date, end_date)
                )

    if dict_bool:
        for key in dict_bool:
            base_query = base_query.filter(getattr(Schema, key) == dict_bool[key])

    if offset == -1:
        data = base_query.all()
    else:
        offsetAfter = offset * page_size
        data = (
            base_query.order_by(desc(getattr(Schema, "modified_at")))
            .offset(offsetAfter)
            .limit(page_size)
            .all()
        )
    total = base_query.count()
    return data, total


def helper_create_parent(Schema, db, data, SchemaChild, child, token):
    try:
        tokenDecode = decode_token(token)
        data["created_by"] = tokenDecode.get("username")
        data["modified_by"] = tokenDecode.get("username")
        ns = Schema(**data)
        db.add(ns)
        db.commit()

        db.refresh(ns)
        if child:
            for a in child:
                if "id" in a:
                    del a["id"]
                ns.children.append(SchemaChild(**a))
                db.commit()

        return ns

    except Exception as e:
        print(e)
        err = e.args[0].split("\n")
        data = {"message": err[errArray(len(err))]}
        raise HandlerCustom(data=data)


def helper_update_parent(Schema, db, data, values, token):
    try:
        tokenDecode = decode_token(token)
        data["modified_by"] = tokenDecode.get("username")
        ns = db.query(Schema).filter_by(id=data["id"]).first()
        for key, value in data.items():
            if key in values:
                setattr(ns, key, value)
        db.commit()
        return ns

    except Exception as e:
        err = e.args[0].split("\n")
        data = {"message": err[errArray(len(err))]}
        raise HandlerCustom(data=data)


def helper_update_child(
    Schema,
    db,
    data,
    values,
    parent,
):
    try:
        if "copyId" in data:
            check = db.query(Schema).filter_by(id=data["copyId"]).first()
            del data["copyId"]
            if check:
                for key, value in data.items():
                    if key in values:
                        setattr(check, key, value)
            else:
                if "id" in data:
                    del data["id"]
                parent.children.append(Schema(**data))
        else:
            if "id" in data:
                del data["id"]
            parent.children.append(Schema(**data))
        db.commit()

    except Exception as e:
        print(e)
        err = e.args[0].split("\n")
        data = {"message": err[errArray(len(err))]}
        raise HandlerCustom(data=data)


def helper_naming_series(connection, target, field, module):
    session = tempSessionn(connection)

    url = os.environ.get("SERVICE_USER") + "get-naming"
    payload = {"module_name": module}
    response = requests.request("POST", url, data=payload)

    res = json.loads(response.text)
    print(res["code"])
    if res["code"] == 200:
        setattr(target, field, res["data"])
    else:
        raise Exception("Please set naming series fix for {0}".format(module))


def check_access_module(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        token = kwargs.get("token")
        if token is not None:
            tokenDecode = decode_token(token)
            request = kwargs.get("request")
            module = kwargs.get("module_access")
            checkRoleExist = r2.exists(tokenDecode["role_id"])
            if checkRoleExist:
                dataAccess = r2.get(tokenDecode["role_id"]).decode("utf-8")
                resultAccess = [
                    d for d in json.loads(dataAccess) if d["module"] == module
                ]
                if resultAccess:
                    if request.method == "POST" and not resultAccess[0]["add"]:
                        raise HandlerCustom(
                            data={
                                "message": "Your don't have access to add this module"
                            }
                        )
                    elif request.method == "PUT" and not resultAccess[0]["edit"]:
                        raise HandlerCustom(
                            data={
                                "message": "Your don't have access to update this module"
                            }
                        )
                    elif request.method == "GET" and not resultAccess[0]["view"]:
                        raise HandlerCustom(
                            data={
                                "message": "Your don't have access to view this module"
                            }
                        )
                else:
                    raise HandlerCustom(data={"message": "Module Not Found"})
            else:
                raise HandlerCustom(data={"message": "Role Not Found"})

        else:
            raise HandlerCustom(data={"message": "must provided by token"})

        return await func(*args, **kwargs)

    return wrapper


def help_filter(request):
    filtered_data = {}
    if request.query_params:
        data_params = dict(request.query_params)
        for key in data_params:
            if key != "page":
                try:
                    filtered_data[key] = int(data_params[key])
                except ValueError:
                    filtered_data[key] = str(data_params[key])
    return filtered_data
