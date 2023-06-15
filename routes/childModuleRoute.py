from fastapi import Request
from fastapi import Depends, status, Header

from controller import childModule
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getCID, getUsername
from db.database import Session
from db.schemas.childModuleSchema import (
    ChildModuleResponseSchema,
    ChildModuleCreateSchema,
    ChildModuleUpdateSchema,
    ChildModuleDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

MODULE_NAME = "child-module"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(MODULE_NAME + "s", response_model=ChildModuleResponseSchema)
# @check_access_module
async def get_all_kurikulum(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = childModule.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered child module",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = childModule.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all child module",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(MODULE_NAME + "/{id}", response_model=ChildModuleResponseSchema)
# @check_access_module
async def get_kurikulum(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = childModule.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get child module",
        "data": data,
    }


@app.post(MODULE_NAME, response_model=ChildModuleResponseSchema)
# @check_access_module
async def submit_kurikulum(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: ChildModuleCreateSchema = None,
):
    username = getUsername(token)

    res = childModule.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit child module",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit child module",
        }


@app.put(MODULE_NAME, response_model=ChildModuleResponseSchema)
# @check_access_module
async def update_kurikulum(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: ChildModuleUpdateSchema = None,
):
    username = getUsername(token)
    res = childModule.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update child module",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update child module",
        }


@app.delete(MODULE_NAME)
# @check_access_module
async def delete_kurikulum(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: ChildModuleDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete child module",
    }
