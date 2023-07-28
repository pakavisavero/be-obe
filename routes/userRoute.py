from fastapi import Request
from fastapi import Depends, status, Header

from controller import user
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.schemas.userSchema import (
    UserResponseSchema,
    UserCreateSchema,
    UserUpdateSchema,
    UserDeleteSchema,
)

USER = "/api/user"
MODULE_NAME = "Users"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(USER + "s", response_model=UserResponseSchema)
# @check_access_module
async def get_all_user(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
    module_access=MODULE_NAME,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = user.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered user",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = user.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all user",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(USER + "/{id}", response_model=UserResponseSchema)
# @check_access_module
async def get_user(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
    request: Request = None,
    module_access=MODULE_NAME,
):
    data = user.getByID(db, id)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get user",
        "data": data,
    }


@app.post(USER, response_model=UserResponseSchema)
# @check_access_module
async def submit_user(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
    request: Request = None,
    module_access=MODULE_NAME,
):
    username = getUsername(token)
    res = user.create(db, username, data)

    if res['status']:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit user",
            "data": res['data'],
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": res['message'],
        }


@app.put(USER, response_model=UserResponseSchema)
# @check_access_module
async def update_user(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
    request: Request = None,
    module_access=MODULE_NAME,
):
    username = getUsername(token)
    res = user.update(db, username, data)
    if res['status']:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update user",
            "data": res['data'],
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": res['message'],
        }


@app.put("/api/update-password", response_model=UserResponseSchema)
# @check_access_module
async def update_password(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
    request: Request = None,
    module_access=MODULE_NAME,
):
    username = getUsername(token)
    res = user.updatePassword(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update user password",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": res,
        }


@app.delete(USER)
async def delete_user(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: UserDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete user",
    }
