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

from HandlerCustom import HandlerCustom
from db.helper import decode_token

USER = "/user"


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


@app.get("/dosens", response_model=UserResponseSchema)
# @check_access_module
async def get_all_dosen(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = user.getAllPagingFilteredSpecialDosen(
            db, page, filtered_data, token, {"role_id": 3}
        )
        data = user.getOnlyDosen(db, query["data"])

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered dosen",
            "data": data,
            "total": query["total"],
        }
    else:
        query = user.getAllPaging(db, page, token)
        data = user.getOnlyDosen(db, query["data"])

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all dosen",
            "data": data,
            "total": query["total"],
        }


@app.get(USER + "/{id}", response_model=UserResponseSchema)
# @check_access_module
async def get_user(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = user.getByID(db, id, token)
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
    data: UserCreateSchema = None,
):
    username = getUsername(token)

    res = user.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit user",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit user",
        }


@app.put(USER, response_model=UserResponseSchema)
# @check_access_module
async def update_user(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: UserUpdateSchema = None,
):
    username = getUsername(token)
    res = user.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update user",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update user",
        }


@app.delete(USER)
# @check_access_module
async def delete_user(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: UserDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete user",
    }
