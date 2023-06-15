from fastapi import Request
from fastapi import Depends, status, Header

from controller import cpl
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.schemas.cplSchema import (
    CPLResponseSchema,
    CPLCreateSchema,
    CPLUpdateSchema,
    CPLDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

CPL = "/cpl"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(CPL + "s", response_model=CPLResponseSchema)
# @check_access_module
async def get_all_cpl(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = cpl.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered cpl",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = cpl.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all cpl",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(CPL + "/{id}", response_model=CPLResponseSchema)
# @check_access_module
async def get_cpl(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = cpl.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get cpl",
        "data": data,
    }


@app.post(CPL, response_model=CPLResponseSchema)
# @check_access_module
async def submit_cpl(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: CPLCreateSchema = None,
):
    username = getUsername(token)

    res = cpl.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit cpl",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit cpl",
        }


@app.put(CPL, response_model=CPLResponseSchema)
# @check_access_module
async def update_cpl(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: CPLUpdateSchema = None,
):
    username = getUsername(token)
    res = cpl.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update cpl",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update cpl",
        }


@app.delete(CPL)
# @check_access_module
async def delete_cpl(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: CPLDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete cpl",
    }
