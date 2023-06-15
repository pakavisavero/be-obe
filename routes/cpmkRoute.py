from fastapi import Request
from fastapi import Depends, status, Header

from controller import cpmk
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getCID, getUsername
from db.database import Session
from db.schemas.cpmkSchema import (
    CPMKResponseSchema,
    CPMKCreateSchema,
    CPMKUpdateSchema,
    CPMKDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

MODULE_NAME = "cpmk"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(MODULE_NAME + "s", response_model=CPMKResponseSchema)
# @check_access_module
async def get_all_cpmk(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = cpmk.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered cpmk",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = cpmk.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all cpmk",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(MODULE_NAME + "/{id}", response_model=CPMKResponseSchema)
# @check_access_module
async def get_cpmk(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = cpmk.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get cpmk",
        "data": data,
    }


@app.post(MODULE_NAME, response_model=CPMKResponseSchema)
# @check_access_module
async def submit_cpmk(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: CPMKCreateSchema = None,
):
    username = getUsername(token)

    res = cpmk.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit cpmk",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit cpmk",
        }


@app.put(MODULE_NAME, response_model=CPMKResponseSchema)
# @check_access_module
async def update_cpmk(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: CPMKUpdateSchema = None,
):
    username = getUsername(token)
    res = cpmk.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update cpmk",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update cpmk",
        }


@app.delete(MODULE_NAME)
# @check_access_module
async def delete_cpmk(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: CPMKDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete cpmk",
    }
