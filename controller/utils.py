from fastapi.responses import JSONResponse
from fastapi import status

from datetime import datetime, timedelta
from sqlalchemy import cast, String, Date, desc, or_
from HandlerCustom import HandlerCustom
from functools import wraps
from db.middleware import r, r2, decode_user_access, decode_token
import jwt
from enum import Enum
from db.models import *

from math import ceil
from openpyxl.utils import get_column_letter
import pandas as pd
from datetime import datetime, timedelta
import time


class DocStatus(Enum):
    MENUNGGU_UPLOAD_DPNA = 1
    MENUNGGU_UPLOAD_CPMK = 2
    SELESAI = 3


def error_handling(e):
    error = str(e)
    if 'message' in e.args[0]:
        error = e.args[0]['message']

    return {
        'status': False,
        'message': error
    }


def remove_char(text: str):
    text = text.split(" ")
    length = len(text)
    text = text[length - 1]

    char = ["(", ")"]
    for c in char:
        text = text.replace(c, "")

    return text.strip()


def is_foreign_key(column):
    return True if column.foreign_keys else False


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


def changeBoll(name):
    if name == "true":
        return True

    return False


def decodeToken(token):
    return jwt.decode(token, "SECRET", algorithms=["HS256"])


def identifyRole(token):
    token = decode_token(token)
    return token


def helper_static_filter(db, Schema, filtered, offset, xtra={}, xtraOr={}):
    page_size = 10
    is_paging = True
    dict_string = {}
    dict_number = {}
    dict_bool = {}
    dict_not_null = {}
    list_dates = []
    key_dates = ""
    base_query = db.query(Schema)

    if xtraOr != {}:
        base_query = base_query.filter(xtraOr)

    for key in filtered:
        if key == "page_size":
            page_size = filtered[key]

        else:
            if filtered[key] == "not null":
                dict_not_null[key] = str(filtered[key])
            else:
                if isinstance(filtered[key], int):
                    dict_number[key] = int(filtered[key])

                if isinstance(filtered[key], str):
                    if str(filtered[key]) in ["true", "false"]:
                        if str(key) == "is_paging":
                            is_paging = changeBoll(str(filtered[key]))

                        dict_bool[key] = changeBoll(str(filtered[key]))

                    else:
                        dict_string[key] = str(filtered[key])

    if dict_number:
        for key in dict_number:
            if dict_number[key]:
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
                if "[" in str(key):
                    key_split = str(key).split("[")
                    key_dates = key_split[0]
                    list_dates.append(dict_string[key])
                else:
                    base_query = base_query.filter(
                        getattr(Schema, key).ilike(
                            "%{}%".format(dict_string[key]))
                    )

    if key_dates and len(list_dates) == 2:
        start_date = datetime.strptime(
            list_dates[0][:10], "%Y-%m-%d"
        ).date() + timedelta(days=1)
        end_date = datetime.strptime(list_dates[1][:10], "%Y-%m-%d").date() + timedelta(
            days=1
        )
        if list_dates[0] == list_dates[1]:
            base_query = base_query.filter(
                cast(getattr(Schema, key_dates), Date) == start_date
            )
        else:
            base_query = base_query.filter(
                or_(
                    cast(getattr(Schema, key_dates), Date) == start_date,
                    cast(getattr(Schema, key_dates), Date).between(
                        start_date, end_date
                    ),
                )
            )

    if dict_bool:
        for key in dict_bool:
            if key != 'is_paging':
                if dict_bool[key] == True or dict_bool[key] == False:
                    base_query = base_query.filter(
                        getattr(Schema, key) == dict_bool[key])

    if dict_not_null:
        for key in dict_not_null:
            if dict_not_null[key]:
                print(dict_not_null[key])
                base_query = base_query.filter(
                    getattr(Schema, key).isnot(None))

    if is_paging == False:
        data = (
            base_query.filter_by(
                **xtra).order_by(desc("modified_at")).limit(50).all()
        )
        total = base_query.count()
        return data, total

    else:
        if offset == -1:
            data = base_query.order_by(desc("modified_at")).all()

        else:
            offsetAfter = offset * page_size
            if page_size == 0:
                data = base_query.filter_by(
                    **xtra).order_by(desc("modified_at")).all()
            else:
                data = (
                    base_query.filter_by(**xtra)
                    .order_by(desc("modified_at"))
                    .offset(offsetAfter)
                    .limit(page_size)
                    .all()
                )

        total = base_query.count()
        return data, total


def helper_create(Schema, db, data):
    try:
        ns = Schema(**data.dict())
        db.add(ns)
        db.commit()

        return ns

    except Exception as e:
        err = e.args[0].split("\n")
        data = {"message": err[errArray(len(err))]}
        raise HandlerCustom(data=data)


def helper_update(Schema, db, data, cb):
    try:
        (db.query(Schema).filter_by(id=data.id).update(dict(data)))

        db.commit()
        return cb(db, data.id)

    except Exception as e:
        err = e.args[0].split("\n")
        data = {"message": err[errArray(len(err))]}
        print(e)
        raise HandlerCustom(data=data)


def helper_update_parent(Schema, db, data, values):
    try:
        ns = db.query(Schema).filter_by(id=data["id"]).first()
        for key, value in data.items():
            if key in values:
                setattr(ns, key, value)
        db.commit()
        return ns

    except Exception as e:
        print(e)
        err = e.args[0].split("\n")
        data = {"message": err[errArray(len(err))]}
        raise HandlerCustom(data=data)


def help_filter(request):
    filtered_data = {}
    if request.query_params:
        data_params = dict(request.query_params)
        for key in data_params:
            if (
                key != "page"
            ):
                try:
                    filtered_data[key] = int(data_params[key])
                except ValueError:
                    filtered_data[key] = str(data_params[key])

    return filtered_data


def helper_create_parent_multi_child(Schema, db, data, childs):
    try:
        ns = Schema(**data)
        db.add(ns)
        db.commit()

        for child in childs:
            if child["data"]:
                for detail in child["data"]:
                    if "id" in detail:
                        del detail["id"]
                    getattr(ns, child["name"]).append(
                        child["schema"](**detail))

        db.commit()

        return ns

    except Exception as e:
        print(e)
        err = e.args[0].split("\n")
        data = {"message": err[errArray(len(err))]}
        raise HandlerCustom(data=data)


def helper_update_multi_child(Schema, db, data, values, parent, nameChild):
    try:
        if "copyId" in data:
            check = db.query(Schema).filter_by(id=data["copyId"]).first()
            del data["copyId"]
            if check:
                for key, value in data.items():
                    if key in values:
                        setattr(check, key, value)
            else:
                getattr(parent, nameChild).append(Schema(**data))
        else:
            getattr(parent, nameChild).append(Schema(**data))
        db.commit()

    except Exception as e:
        err = e.args[0].split("\n")
        data = {"message": err[errArray(len(err))]}
        raise HandlerCustom(data=data)


def check_access_module(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        token = decode_token(kwargs.get("token"), True)
        request = kwargs.get("request")
        db = kwargs.get("db")
        module = kwargs.get("module_access")
        action = ""

        user = db.query(User).filter_by(id=token.get("user_id")).first()
        if user:
            module_id = db.query(Module).filter_by(module_name=module).first()
            if module_id:
                if request.method == "POST":
                    action = "add"

                elif request.method == "PUT":
                    action = "edit"

                elif request.method == "GET":
                    action = "view"

                granted = (
                    db.query(RolePermission)
                    .filter_by(module_id=module_id.id)
                    .filter_by(role_id=token.get("role_id"))
                    .first()
                )

                if not getattr(granted, action):
                    raise HandlerCustom(
                        data={
                            "message": "Your don't have access to {0} this module".format(
                                action
                            )
                        }
                    )
            else:
                raise HandlerCustom(data={"message": "Module not found"})

        else:
            raise HandlerCustom(data={"message": "User not found"})

        return await func(*args, **kwargs)

    return wrapper


def to_dict(is_parent=True, row=[], modified=[], xtraIgnore=[]):
    ignores = ['id', 'is_active', 'created_at',
               'created_by', 'modified_at', 'modified_by']
    ignores.extend(xtraIgnore)

    if row is None:
        return None

    rtn_dict = dict()
    keys = row.__table__.columns.keys()

    for key in keys:
        if not key in ignores:
            rtn_dict[key] = getattr(row, key)
            if is_parent:
                for mod in modified:
                    if 'name' in mod:
                        relation = to_dict(
                            is_parent=False,
                            row=getattr(row, mod['relation'])
                        )

                        if relation:
                            rtn_dict[mod['name']] = relation[mod['opt']]
                        else:
                            rtn_dict[mod['name']] = '-'

    return rtn_dict


def export_file(columns, element, filename):
    df = pd.DataFrame(element)
    date_time = str(time.mktime(
                    datetime.now().timetuple()))
    file_response = "export_files/{}".format(filename) + \
        "_" + date_time + ".xlsx"

    writer = pd.ExcelWriter(file_response)

    df.columns = columns
    df.index = df.index + 1
    df.to_excel(writer)
    writer.save()

    return file_response
