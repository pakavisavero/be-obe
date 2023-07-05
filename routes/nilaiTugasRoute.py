from fastapi import Request
from fastapi import Depends, status, Header

from controller import nilaiTugas
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.schemas.nilaiTugasSchema import (
    NilaiTugasResponseSchema,
    NilaiTugasCreateSchema,
    NilaiTugasUpdateSchema,
    NilaiTugasDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

NILAI_TUGAS = "/nilai-tugas"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(NILAI_TUGAS + "es", response_model=NilaiTugasResponseSchema)
# @check_access_module
async def get_all_nilai_tugas(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = nilaiTugas.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered nilai tugas",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = nilaiTugas.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all nilai tugas",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(NILAI_TUGAS + "/{id}", response_model=NilaiTugasResponseSchema)
# @check_access_module
async def get_nilai_tugas(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = nilaiTugas.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get nilai tugas",
        "data": data,
    }


@app.post(NILAI_TUGAS, response_model=NilaiTugasResponseSchema)
# @check_access_module
async def submit_nilai_tugas(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: NilaiTugasCreateSchema = None,
):
    username = getUsername(token)

    res = nilaiTugas.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit nilai tugas",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit nilai tugas",
        }


@app.put(NILAI_TUGAS, response_model=NilaiTugasResponseSchema)
# @check_access_module
async def update_nilai_tugas(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: NilaiTugasUpdateSchema = None,
):
    username = getUsername(token)
    res = nilaiTugas.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update nilai tugas",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update nilai tugas",
        }


@app.delete(NILAI_TUGAS)
# @check_access_module
async def delete_nilai_tugas(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: NilaiTugasDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete nilai tugas",
    }
