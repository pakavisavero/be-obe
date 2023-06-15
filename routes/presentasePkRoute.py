from fastapi import Request
from fastapi import Depends, status, Header

from controller import PresentasePK
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getCID, getUsername
from db.database import Session
from db.schemas.cplSchema import (
    CPLResponseSchema,
    CPLCreateSchema,
    CPLUpdateSchema,
    CPLDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

MODULE_NAME = "presentase-pk"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(MODULE_NAME + "s", response_model=CPLResponseSchema)
# @check_access_module
async def get_all_presentase_pk(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = PresentasePK.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered presentase pk",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = PresentasePK.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all presentase pk",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(MODULE_NAME + "/{id}", response_model=CPLResponseSchema)
# @check_access_module
async def get_presentase_pk(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = PresentasePK.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get presentase pk",
        "data": data,
    }


@app.post(MODULE_NAME, response_model=CPLResponseSchema)
# @check_access_module
async def submit_presentase_pk(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: CPLCreateSchema = None,
):
    username = getUsername(token)

    res = PresentasePK.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit presentase pk",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit presentase pk",
        }


@app.put(MODULE_NAME, response_model=CPLResponseSchema)
# @check_access_module
async def update_presentase_pk(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: CPLUpdateSchema = None,
):
    username = getUsername(token)
    res = PresentasePK.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update presentase pk",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update presentase pk",
        }


@app.delete(MODULE_NAME)
# @check_access_module
async def delete_presentase_pk(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: CPLDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete presentase pk",
    }
