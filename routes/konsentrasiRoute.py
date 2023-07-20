from fastapi import Request
from fastapi import Depends, status, Header

from controller import konsentrasi
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.schemas.konsentrasiSchema import (
    KonsentrasiResponseSchema,
    KonsentrasiCreateSchema,
    KonsentrasiUpdateSchema,
    KonsentrasiDeleteSchema,
)

KONSENTRASI = "/api/konsentrasi"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(KONSENTRASI + "s", response_model=KonsentrasiResponseSchema)
# @check_access_module
async def get_all_konsentrasi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = konsentrasi.getAllPagingFiltered(
            db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered konsentrasi",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = konsentrasi.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all konsentrasi",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(KONSENTRASI + "/{id}", response_model=KonsentrasiResponseSchema)
# @check_access_module
async def get_konsentrasi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = konsentrasi.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get konsentrasi",
        "data": data,
    }


@app.post(KONSENTRASI, response_model=KonsentrasiResponseSchema)
# @check_access_module
async def submit_konsentrasi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: KonsentrasiCreateSchema = None,
):
    username = getUsername(token)

    res = konsentrasi.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit konsentrasi",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit konsentrasi",
        }


@app.put(KONSENTRASI, response_model=KonsentrasiResponseSchema)
# @check_access_module
async def update_konsentrasi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: KonsentrasiUpdateSchema = None,
):
    username = getUsername(token)
    res = konsentrasi.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update konsentrasi",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update konsentrasi",
        }


@app.delete(KONSENTRASI)
# @check_access_module
async def delete_konsentrasi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: KonsentrasiDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete konsentrasi",
    }
