from fastapi import Request
from fastapi import Depends, status, Header

from controller import roleMaster
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.schemas.roleMasterSchema import (
    RoleMasterResponseSchema,
    RoleMasterCreateSchema,
    RoleMasterUpdateSchema,
    RoleMasterDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

ROLE_MASTER = "/api/role-master"
MODULE_NAME = "Role Master"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(ROLE_MASTER + "s", response_model=RoleMasterResponseSchema)
@check_access_module
async def get_all_role_master(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
    module_access=MODULE_NAME,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = roleMaster.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered role master",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = roleMaster.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all role master",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(ROLE_MASTER + "/{id}", response_model=RoleMasterResponseSchema)
@check_access_module
async def get_role_master(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
    request: Request = None,
    module_access=MODULE_NAME,
):
    data = roleMaster.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get role master",
        "data": data,
    }


@app.post(ROLE_MASTER, response_model=RoleMasterResponseSchema)
@check_access_module
async def submit_role_master(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: RoleMasterCreateSchema = None,
    request: Request = None,
    module_access=MODULE_NAME,
):
    username = getUsername(token)

    res = roleMaster.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit role master",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit role master",
        }


@app.put(ROLE_MASTER, response_model=RoleMasterResponseSchema)
@check_access_module
async def update_role_master(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: RoleMasterUpdateSchema = None,
    request: Request = None,
    module_access=MODULE_NAME,
):
    username = getUsername(token)
    res = roleMaster.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update role master",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update role master",
        }


@app.delete(ROLE_MASTER)
async def delete_role_master(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: RoleMasterDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete role master",
    }
