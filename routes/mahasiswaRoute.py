from fastapi import Request
from fastapi import Depends, status, Header

from controller import mahasiswa
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getCID, getUsername
from db.database import Session
from db.schemas.mahasiswaSchema import (
    MahasiswaResponseSchema,
    MahasiswaCreateSchema,
    MahasiswaUpdateSchema,
    MahasiswaDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

MODULE_NAME = "mahasiswa"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(MODULE_NAME + "s", response_model=MahasiswaResponseSchema)
# @check_access_module
async def get_all_mahasiswa(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = mahasiswa.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered mahasiswa",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = mahasiswa.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all mahasiswa",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(MODULE_NAME + "/{id}", response_model=MahasiswaResponseSchema)
# @check_access_module
async def get_mahasiswa(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = mahasiswa.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get mahasiswa",
        "data": data,
    }


@app.post(MODULE_NAME, response_model=MahasiswaResponseSchema)
# @check_access_module
async def submit_mahasiswa(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MahasiswaCreateSchema = None,
):
    username = getUsername(token)

    res = mahasiswa.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit mahasiswa",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit mahasiswa",
        }


@app.put(MODULE_NAME, response_model=MahasiswaResponseSchema)
# @check_access_module
async def update_mahasiswa(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MahasiswaUpdateSchema = None,
):
    username = getUsername(token)
    res = mahasiswa.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update mahasiswa",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update mahasiswa",
        }


@app.delete(MODULE_NAME)
# @check_access_module
async def delete_mahasiswa(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MahasiswaDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete mahasiswa",
    }
