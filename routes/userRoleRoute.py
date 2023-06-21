from fastapi import Request
from fastapi import Depends, status, Header

from controller import userRole
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.schemas.userRoleSchema import (
    UserRoleResponseSchema,
    UserRoleCreateSchema,
    UserRoleUpdateSchema,
    UserRoleDeleteSchema,
)

USER_ROLE = "/user-role"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(USER_ROLE + "s", response_model=UserRoleResponseSchema)
@check_access_module
async def get_all_user_role(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = userRole.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered user role",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = userRole.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all user role",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(USER_ROLE + "/{id}", response_model=UserRoleResponseSchema)
@check_access_module
async def get_user_role(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = userRole.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get user role",
        "data": data,
    }


@app.post(USER_ROLE, response_model=UserRoleResponseSchema)
@check_access_module
async def submit_user_role(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: UserRoleCreateSchema = None,
):
    username = getUsername(token)

    res = userRole.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit user role",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit user role",
        }


@app.put(USER_ROLE, response_model=UserRoleResponseSchema)
@check_access_module
async def update_user_role(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: UserRoleUpdateSchema = None,
):
    username = getUsername(token)
    res = userRole.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update user role",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update user role",
        }


@app.delete(USER_ROLE)
# @check_access_module
async def delete_user_role(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: UserRoleDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete user role",
    }
