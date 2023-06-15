from fastapi import Request
from fastapi import Depends, status, Header

from controller import statusMahasiswa
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.schemas.statusMahasiswaSchema import (
    StatusMahasiswaResponseSchema,
    StatusMahasiswaCreateSchema,
    StatusMahasiswaUpdateSchema,
    StatusMahasiswaDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

STATUS_MHS = "/status-mahasiswa"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(STATUS_MHS + "s", response_model=StatusMahasiswaResponseSchema)
# @check_access_module
async def get_all_status_mahasiswa(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = statusMahasiswa.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered status mahasiswa",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = statusMahasiswa.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all status mahasiswa",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(STATUS_MHS + "/{id}", response_model=StatusMahasiswaResponseSchema)
# @check_access_module
async def get_status_mahasiswa(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = statusMahasiswa.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get status mahasiswa",
        "data": data,
    }


@app.post(STATUS_MHS, response_model=StatusMahasiswaResponseSchema)
# @check_access_module
async def submit_status_mahasiswa(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: StatusMahasiswaCreateSchema = None,
):
    username = getUsername(token)

    res = statusMahasiswa.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit status mahasiswa",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit status mahasiswa",
        }


@app.put(STATUS_MHS, response_model=StatusMahasiswaResponseSchema)
# @check_access_module
async def update_status_mahasiswa(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: StatusMahasiswaUpdateSchema = None,
):
    username = getUsername(token)
    res = statusMahasiswa.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update status mahasiswa",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update status mahasiswa",
        }


@app.delete(STATUS_MHS)
# @check_access_module
async def delete_status_mahasiswa(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: StatusMahasiswaDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete status mahasiswa",
    }
