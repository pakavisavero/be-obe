from datetime import datetime, timedelta
from sqlalchemy import cast, String, Date, desc, or_

from HandlerCustom import HandlerCustom
from functools import wraps
import jwt
from fastapi.responses import JSONResponse
from fastapi import status
import redis
import json


r = redis.Redis(host="localhost", port=6379, db=5)
r2 = redis.Redis(host="localhost", port=6379, db=6)


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


def check_access_module(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        token = kwargs.get("token")
        if not token:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "message": "Missing token",
                },
            )
        user = decodeToken(token)
        role_id = user.get("role_id")
        try:
            r_check = r.exists(token)
            r2_check = r2.exists(role_id)
            if not r2_check or not r_check:
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={
                        "message": "Access denied",
                    },
                )

            return await func(*args, **kwargs)

        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": str(e)},
            )

    return wrapper


def helper_static_filter(db, Schema, cid, filtered, offset, xtra={}):
    page_size = 10
    is_paging = True
    dict_string = {}
    dict_number = {}
    dict_bool = {}
    dict_not_null = {}
    list_dates = []
    key_dates = ""
    base_query = db.query(Schema)

    if cid:
        base_query = base_query.filter_by(client_id=cid)

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
                        getattr(Schema, key).ilike("%{}%".format(dict_string[key]))
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
            if dict_bool[key] == True or dict_bool[key] == False:
                base_query = base_query.filter(getattr(Schema, key) == dict_bool[key])

    if dict_not_null:
        for key in dict_not_null:
            if dict_not_null[key]:
                print(dict_not_null[key])
                base_query = base_query.filter(getattr(Schema, key).isnot(None))
                # base_query = base_query.filter(
                #     getattr(Schema, key) == dict_number[key]
                # )
    # data = (
    #     base_query
    #     .order_by(desc(getattr(Schema, desc("modified_at"))))
    #     .offset(offset)
    #     .limit(10)
    #     .all()
    # )

    if is_paging == False:
        data = (
            base_query.filter_by(**xtra).limit(50).order_by(desc("modified_at")).all()
        )
        total = base_query.count()
        return data, total

    else:
        if offset == -1:
            data = base_query.order_by(desc("modified_at")).all()

        else:
            offsetAfter = offset * page_size
            if page_size == 0:
                data = base_query.filter_by(**xtra).order_by(desc("modified_at")).all()
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


def helper_update(Schema, db, cid, data, cb):
    try:
        (
            db.query(Schema)
            .filter_by(client_id=cid)
            .filter_by(id=data.id)
            .update(dict(data))
        )

        db.commit()
        return cb(db, cid, data.id)

    except Exception as e:
        err = e.args[0].split("\n")
        data = {"message": err[errArray(len(err))]}
        print(e)
        raise HandlerCustom(data=data)


# Create Parent Contract
def helper_create_parent_contract(Schema, db, data, SchemaChild, child):
    try:
        ns = Schema(**data)
        db.add(ns)
        db.commit()

        if child:
            for a in child:
                if "id" in a:
                    del a["id"]
                ns.attachment.append(SchemaChild(**a))

        db.commit()

        return ns

    except Exception as e:
        print(e)
        err = e.args[0].split("\n")
        data = {"message": err[errArray(len(err))]}
        raise HandlerCustom(data=data)


# Create Parent SLA


def helper_create_parent_sla(Schema, db, data, SchemaChild, child):
    try:
        print(data)
        ns = Schema(**data)
        db.add(ns)
        db.commit()

        if child:
            for a in child:
                if "id" in a:
                    del a["id"]
                ns.slaDetail.append(SchemaChild(**a))

        db.commit()

        return ns

    except Exception as e:
        print(e)
        err = e.args[0].split("\n")
        data = {"message": err[errArray(len(err))]}
        raise HandlerCustom(data=data)


# Create Parent Stock Warranty
def helper_create_parent_stock_warranty(Schema, db, data, SchemaChild, child):
    try:
        ns = Schema(**data)
        db.add(ns)
        db.commit()

        if child:
            for a in child:
                if "id" in a:
                    del a["id"]
                ns.warranty_serial.append(SchemaChild(**a))

        db.commit()

        return ns

    except Exception as e:
        print(e)
        err = e.args[0].split("\n")
        data = {"message": err[errArray(len(err))]}
        raise HandlerCustom(data=data)


# Create Parent Contract
def helper_create_parent_contract_pm(Schema, db, data, SchemaChild, child):
    try:
        ns = Schema(**data)
        db.add(ns)
        db.commit()

        if child:
            for a in child:
                if "id" in a:
                    del a["id"]
                ns.period.append(SchemaChild(**a))

        db.commit()

        return ns

    except Exception as e:
        print(e)
        err = e.args[0].split("\n")
        data = {"message": err[errArray(len(err))]}
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


def helper_update_sla(
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
                parent.slaDetail.append(Schema(**data))
        else:
            parent.slaDetail.append(Schema(**data))

        db.commit()

    except Exception as e:
        err = e.args[0].split("\n")
        data = {"message": err[errArray(len(err))]}
        raise HandlerCustom(data=data)


def helper_update_stock_warranty(
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
                parent.warranty_serial.append(Schema(**data))
        else:
            parent.warranty_serial.append(Schema(**data))

        db.commit()

    except Exception as e:
        err = e.args[0].split("\n")
        data = {"message": err[errArray(len(err))]}
        raise HandlerCustom(data=data)


def helper_update_pm_plan(
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
                parent.period.append(Schema(**data))
        else:
            parent.period.append(Schema(**data))

        db.commit()

    except Exception as e:
        err = e.args[0].split("\n")
        data = {"message": err[errArray(len(err))]}
        raise HandlerCustom(data=data)


def helper_update_contract(
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
                parent.attachment.append(Schema(**data))
        else:
            parent.attachment.append(Schema(**data))
        db.commit()

    except Exception as e:
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
                and key != "is_aso"
                and key != "is_paging"
                and key != "main_unit"
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
                    getattr(ns, child["name"]).append(child["schema"](**detail))

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
