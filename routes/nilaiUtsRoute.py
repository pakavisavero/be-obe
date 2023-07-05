from fastapi import Request
from fastapi import Depends, status, Header

from controller import nilaiUts
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.schemas.nilaiUtsSchema import (
    NilaiUtsResponseSchema,
    NilaiUtsCreateSchema,
    NilaiUtsUpdateSchema,
    NilaiUtsDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

NILAI_UTS = "/nilai-uts"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(NILAI_UTS + "es", response_model=NilaiUtsResponseSchema)
# @check_access_module
async def get_all_nilai_uts(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = nilaiUts.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered nilai uts",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = nilaiUts.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all nilai uts",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(NILAI_UTS + "/{id}", response_model=NilaiUtsResponseSchema)
# @check_access_module
async def get_nilai_uts(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = nilaiUts.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get nilai uts",
        "data": data,
    }


@app.post(NILAI_UTS, response_model=NilaiUtsResponseSchema)
# @check_access_module
async def submit_nilai_uts(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: NilaiUtsCreateSchema = None,
):
    username = getUsername(token)

    res = nilaiUts.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit nilai uts",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit nilai uts",
        }


@app.put(NILAI_UTS, response_model=NilaiUtsResponseSchema)
# @check_access_module
async def update_nilai_uts(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: NilaiUtsUpdateSchema = None,
):
    username = getUsername(token)
    res = nilaiUts.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update nilai uts",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update nilai uts",
        }


@app.delete(NILAI_UTS)
# @check_access_module
async def delete_nilai_uts(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: NilaiUtsDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete nilai uts",
    }
