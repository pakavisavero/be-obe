from fastapi import Request
from fastapi import Depends, status, Header

from controller import konsentrasiProdi
from routes.route import app
from controller.utils import help_filter

from db.session import db, getUsername
from db.database import Session
from db.schemas.konsentrasiProdiSchema import (
    KonsentrasiProdiResponseSchema,
    KonsentrasiProdiCreateSchema,
    KonsentrasiProdiUpdateSchema,
    KonsentrasiProdiDeleteSchema,
)

KONSENTRASI_PRODI = "/konsentrasi-prodi"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(KONSENTRASI_PRODI + "s", response_model=KonsentrasiProdiResponseSchema)
# @check_access_module
async def get_all_modules(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = konsentrasiProdi.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered konsentrasi prodi",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = konsentrasiProdi.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all konsentrasi prodi",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(KONSENTRASI_PRODI + "/{id}", response_model=KonsentrasiProdiResponseSchema)
# @check_access_module
async def get_module(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = konsentrasiProdi.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get konsentrasi prodi",
        "data": data,
    }


@app.post(KONSENTRASI_PRODI, response_model=KonsentrasiProdiResponseSchema)
# @check_access_module
async def submit_module(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: KonsentrasiProdiCreateSchema = None,
):
    username = getUsername(token)

    res = konsentrasiProdi.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit konsentrasi prodi",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit konsentrasi prodi",
        }


@app.put(KONSENTRASI_PRODI, response_model=KonsentrasiProdiResponseSchema)
# @check_access_module
async def update_module(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: KonsentrasiProdiUpdateSchema = None,
):
    username = getUsername(token)
    res = konsentrasiProdi.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update konsentrasi prodi",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update konsentrasi prodi",
        }


@app.delete(KONSENTRASI_PRODI)
# @check_access_module
async def delete_module(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: KonsentrasiProdiDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete konsentrasi prodi",
    }
