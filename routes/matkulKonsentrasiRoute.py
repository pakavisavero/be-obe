from fastapi import Request
from fastapi import Depends, status, Header

from controller import matkulKonsentrasi
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getCID, getUsername
from db.database import Session
from db.schemas.matkulKonsentrasiSchema import (
    MatkulKonsentrasiResponseSchema,
    MatkulKonsentrasiCreateSchema,
    MatkulKonsentrasiUpdateSchema,
    MatkulKonsentrasiDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

MODULE_NAME = "matkul-konsentrasi"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(MODULE_NAME + "s", response_model=MatkulKonsentrasiResponseSchema)
# @check_access_module
async def get_all_konsentrasi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = matkulKonsentrasi.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered matkul konsentrasi",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = matkulKonsentrasi.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all matkul konsentrasi",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(MODULE_NAME + "/{id}", response_model=MatkulKonsentrasiResponseSchema)
# @check_access_module
async def get_konsentrasi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = matkulKonsentrasi.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get matkul konsentrasi",
        "data": data,
    }


@app.post(MODULE_NAME, response_model=MatkulKonsentrasiResponseSchema)
# @check_access_module
async def submit_konsentrasi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MatkulKonsentrasiCreateSchema = None,
):
    username = getUsername(token)

    res = matkulKonsentrasi.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit matkul konsentrasi",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit matkul konsentrasi",
        }


@app.put(MODULE_NAME, response_model=MatkulKonsentrasiResponseSchema)
# @check_access_module
async def update_konsentrasi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MatkulKonsentrasiUpdateSchema = None,
):
    username = getUsername(token)
    res = matkulKonsentrasi.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update matkul konsentrasi",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update matkul konsentrasi",
        }


@app.delete(MODULE_NAME)
# @check_access_module
async def delete_konsentrasi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MatkulKonsentrasiDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete matkul konsentrasi",
    }
