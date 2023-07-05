from fastapi import Request
from fastapi import Depends, status, Header

from controller import rolePermission
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.schemas.rolePermissionSchema import (
    RolePermissionResponseSchema,
    RolePermissionCreateSchema,
    RolePermissionUpdateSchema,
    RolePermissionDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

ROLE_PERMISSION = "/role-permission"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(ROLE_PERMISSION + "s", response_model=RolePermissionResponseSchema)
# @check_access_module
async def get_all_role_permission(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = rolePermission.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered role permission",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = rolePermission.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all role permission",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(ROLE_PERMISSION + "/{id}", response_model=RolePermissionResponseSchema)
# @check_access_module
async def get_role_permission(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = rolePermission.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get role permission",
        "data": data,
    }


@app.post(ROLE_PERMISSION, response_model=RolePermissionResponseSchema)
# @check_access_module
async def submit_role_permission(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: RolePermissionCreateSchema = None,
):
    username = getUsername(token)

    res = rolePermission.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit role permission",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit role permission",
        }


@app.put(ROLE_PERMISSION, response_model=RolePermissionResponseSchema)
# @check_access_module
async def update_role_permission(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: RolePermissionUpdateSchema = None,
):
    username = getUsername(token)
    res = rolePermission.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update role permission",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update role permission",
        }


@app.delete(ROLE_PERMISSION)
# @check_access_module
async def delete_role_permission(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: RolePermissionDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete role permission",
    }
