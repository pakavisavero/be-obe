from fastapi import Request
from fastapi import Depends, status, Header

from controller import presentasePk
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

PRESENTASE_PK = "/api/presentase-pk"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(PRESENTASE_PK + "s", response_model=CPLResponseSchema)
# @check_access_module
async def get_all_presentase_pk(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = presentasePk.getAllPagingFiltered(
            db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered presentase pk",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = presentasePk.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all presentase pk",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(PRESENTASE_PK + "/{id}", response_model=CPLResponseSchema)
# @check_access_module
async def get_presentase_pk(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = presentasePk.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get presentase pk",
        "data": data,
    }


@app.post(PRESENTASE_PK, response_model=CPLResponseSchema)
# @check_access_module
async def submit_presentase_pk(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: CPLCreateSchema = None,
):
    username = getUsername(token)

    res = presentasePk.create(db, username, data)
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


@app.put(PRESENTASE_PK, response_model=CPLResponseSchema)
# @check_access_module
async def update_presentase_pk(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: CPLUpdateSchema = None,
):
    username = getUsername(token)
    res = presentasePk.update(db, username, data)
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


@app.delete(PRESENTASE_PK)
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
