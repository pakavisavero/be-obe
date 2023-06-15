from fastapi import Request
from fastapi import Depends, status, Header

from controller import mahasiswaDoswal
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getCID, getUsername
from db.database import Session
from db.schemas.mahasiswaDoswalSchema import (
    MahasiswaDoswalResponseSchema,
    MahasiswaDoswalCreateSchema,
    MahasiswaDoswalUpdateSchema,
    MahasiswaDoswalDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

MODULE_NAME = "mahasiswa-doswal"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(MODULE_NAME + "s", response_model=MahasiswaDoswalResponseSchema)
# @check_access_module
async def get_all_mahasiswa_doswal(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = mahasiswaDoswal.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered mahasiswa doswal",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = mahasiswaDoswal.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all mahasiswa doswal",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(MODULE_NAME + "/{id}", response_model=MahasiswaDoswalResponseSchema)
# @check_access_module
async def get_mahasiswa_doswal(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = mahasiswaDoswal.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get mahasiswa doswal",
        "data": data,
    }


@app.post(MODULE_NAME, response_model=MahasiswaDoswalResponseSchema)
# @check_access_module
async def submit_mahasiswa_doswal(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MahasiswaDoswalCreateSchema = None,
):
    username = getUsername(token)

    res = mahasiswaDoswal.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit mahasiswa doswal",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit mahasiswa doswal",
        }


@app.put(MODULE_NAME, response_model=MahasiswaDoswalResponseSchema)
# @check_access_module
async def update_mahasiswa_doswal(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MahasiswaDoswalUpdateSchema = None,
):
    username = getUsername(token)
    res = mahasiswaDoswal.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update mahasiswa doswal",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update mahasiswa doswal",
        }


@app.delete(MODULE_NAME)
# @check_access_module
async def delete_mahasiswa_doswal(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MahasiswaDoswalDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete mahasiswa doswal",
    }
