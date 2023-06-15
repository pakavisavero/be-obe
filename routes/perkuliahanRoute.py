from fastapi import Request
from fastapi import Depends, status, Header

from controller import perkuliahan
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getCID, getUsername
from db.database import Session
from db.schemas.perkuliahanSchema import (
    PerkuliahanResponseSchema,
    PerkuliahanCreateSchema,
    PerkuliahanUpdateSchema,
    PerkuliahanDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

MODULE_NAME = "perkuliahan"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(MODULE_NAME + "s", response_model=PerkuliahanResponseSchema)
# @check_access_module
async def get_all_perkuliahan(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = perkuliahan.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered perkuliahan",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = perkuliahan.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all perkuliahan",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(MODULE_NAME + "/{id}", response_model=PerkuliahanResponseSchema)
# @check_access_module
async def get_perkuliahan(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = perkuliahan.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get perkuliahan",
        "data": data,
    }


@app.post(MODULE_NAME, response_model=PerkuliahanResponseSchema)
# @check_access_module
async def submit_perkuliahan(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: PerkuliahanCreateSchema = None,
):
    username = getUsername(token)

    res = perkuliahan.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit perkuliahan",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit perkuliahan",
        }


@app.put(MODULE_NAME, response_model=PerkuliahanResponseSchema)
# @check_access_module
async def update_perkuliahan(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: PerkuliahanUpdateSchema = None,
):
    username = getUsername(token)
    res = perkuliahan.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update perkuliahan",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update perkuliahan",
        }


@app.delete(MODULE_NAME)
# @check_access_module
async def delete_perkuliahan(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: PerkuliahanDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete perkuliahan",
    }
