from fastapi import Request
from fastapi import Depends, status, Header

from controller import matkulKonsentrasi
from routes.route import app
from controller.utils import help_filter

from db.session import db, getUsername
from db.database import Session
from db.schemas.matkulKonsentrasiSchema import (
    MatkulKonsentrasiResponseSchema,
    MatkulKonsentrasiCreateSchema,
    MatkulKonsentrasiUpdateSchema,
    MatkulKonsentrasiDeleteSchema,
)

MATKUL_KONSENTRASI = "/api/matkul-konsentrasi"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(MATKUL_KONSENTRASI + "s", response_model=MatkulKonsentrasiResponseSchema)
# @check_access_module
async def get_all_konsentrasi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = matkulKonsentrasi.getAllPagingFiltered(
            db, page, filtered_data, token)

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


@app.get(MATKUL_KONSENTRASI + "/{id}", response_model=MatkulKonsentrasiResponseSchema)
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


@app.post(MATKUL_KONSENTRASI, response_model=MatkulKonsentrasiResponseSchema)
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


@app.put(MATKUL_KONSENTRASI, response_model=MatkulKonsentrasiResponseSchema)
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


@app.delete(MATKUL_KONSENTRASI)
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
