from fastapi import Request
from fastapi import Depends, status, Header

from controller import module
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getCID, getUsername
from db.database import Session
from db.schemas.moduleSchema import (
    ModuleResponseSchema,
    ModuleCreateSchema,
    ModuleUpdateSchema,
    ModuleDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

MODULE_NAME = "module"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(MODULE_NAME + "s", response_model=ModuleResponseSchema)
# @check_access_module
async def get_all_modules(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = module.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered module",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = module.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all module",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(MODULE_NAME + "/{id}", response_model=ModuleResponseSchema)
# @check_access_module
async def get_module(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = module.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get module",
        "data": data,
    }


@app.post(MODULE_NAME, response_model=ModuleResponseSchema)
# @check_access_module
async def submit_module(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: ModuleCreateSchema = None,
):
    username = getUsername(token)

    res = module.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit module",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit module",
        }


@app.put(MODULE_NAME, response_model=ModuleResponseSchema)
# @check_access_module
async def update_module(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: ModuleUpdateSchema = None,
):
    username = getUsername(token)
    res = module.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update module",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update module",
        }


@app.delete(MODULE_NAME)
# @check_access_module
async def delete_module(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: ModuleDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete module",
    }
