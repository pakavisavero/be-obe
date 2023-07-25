from fastapi import Request
from fastapi import Depends, status, Header

from controller import module
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.schemas.moduleSchema import (
    ModuleResponseSchema,
    ModuleCreateSchema,
    ModuleUpdateSchema,
    ModuleDeleteSchema,
)

MODULE = "/api/module"
MODULE_NAME = "Module"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(MODULE + "s", response_model=ModuleResponseSchema)
@check_access_module
async def get_all_modules(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
    module_access=MODULE_NAME,
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


@app.get(MODULE + "/{id}", response_model=ModuleResponseSchema)
# @check_access_module
async def get_module(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
    module_access=MODULE_NAME,
):
    data = module.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get module",
        "data": data,
    }


@app.post(MODULE, response_model=ModuleResponseSchema)
@check_access_module
async def submit_module(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: ModuleCreateSchema = None,
    module_access=MODULE_NAME,
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


@app.put(MODULE, response_model=ModuleResponseSchema)
# @check_access_module
async def update_module(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
    module_access=MODULE_NAME,
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


@app.delete(MODULE)
async def delete_module(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: ModuleDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete module",
    }
