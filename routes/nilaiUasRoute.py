from fastapi import Request
from fastapi import Depends, status, Header

from routes.route import app
from controller import nilaiUas
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.schemas.nilaiUasSchema import (
    NilaiUasResponseSchema,
    NilaiUasCreateSchema,
    NilaiUasUpdateSchema,
    NilaiUasDeleteSchema,
)


NILAI_UAS = "/api/nilai-uas"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(NILAI_UAS + "es", response_model=NilaiUasResponseSchema)
# @check_access_module
async def get_all_nilai_uas(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = nilaiUas.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered nilai uas",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = nilaiUas.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all nilai uas",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(NILAI_UAS + "/{id}", response_model=NilaiUasResponseSchema)
# @check_access_module
async def get_nilai_uas(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = nilaiUas.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get nilai uas",
        "data": data,
    }


@app.post(NILAI_UAS, response_model=NilaiUasResponseSchema)
# @check_access_module
async def submit_nilai_uas(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: NilaiUasCreateSchema = None,
):
    username = getUsername(token)

    res = nilaiUas.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit nilai uas",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit nilai uas",
        }


@app.put(NILAI_UAS, response_model=NilaiUasResponseSchema)
# @check_access_module
async def update_nilai_uas(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: NilaiUasUpdateSchema = None,
):
    username = getUsername(token)
    res = nilaiUas.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update nilai uas",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update nilai uas",
        }


@app.delete(NILAI_UAS)
# @check_access_module
async def delete_nilai_uas(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: NilaiUasDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete nilai uas",
    }
