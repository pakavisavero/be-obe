from fastapi import Request
from fastapi import Depends, status, Header

from controller import mahasiswaKonsentrasi
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.schemas.mahasiswaKonsentrasiSchema import (
    MahasiswaKonsentrasiResponseSchema,
    MahasiswaKonsentrasiCreateSchema,
    MahasiswaKonsentrasiUpdateSchema,
    MahasiswaKonsentrasiDeleteSchema,
)


MAHASISWA_KONSENTRASI = "/mahasiswa-konsentrasi"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(MAHASISWA_KONSENTRASI + "s", response_model=MahasiswaKonsentrasiResponseSchema)
# @check_access_module
async def get_all_konsentrasi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = mahasiswaKonsentrasi.getAllPagingFiltered(
            db, page, filtered_data, token
        )

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered mahasiswa konsentrasi",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = mahasiswaKonsentrasi.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all mahasiswa konsentrasi",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(
    MAHASISWA_KONSENTRASI + "/{id}", response_model=MahasiswaKonsentrasiResponseSchema
)
# @check_access_module
async def get_konsentrasi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = mahasiswaKonsentrasi.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get mahasiswa konsentrasi",
        "data": data,
    }


@app.post(MAHASISWA_KONSENTRASI, response_model=MahasiswaKonsentrasiResponseSchema)
# @check_access_module
async def submit_konsentrasi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MahasiswaKonsentrasiCreateSchema = None,
):
    username = getUsername(token)

    res = mahasiswaKonsentrasi.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit mahasiswa konsentrasi",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit mahasiswa konsentrasi",
        }


@app.put(MAHASISWA_KONSENTRASI, response_model=MahasiswaKonsentrasiResponseSchema)
# @check_access_module
async def update_konsentrasi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MahasiswaKonsentrasiUpdateSchema = None,
):
    username = getUsername(token)
    res = mahasiswaKonsentrasi.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update mahasiswa konsentrasi",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update mahasiswa konsentrasi",
        }


@app.delete(MAHASISWA_KONSENTRASI)
# @check_access_module
async def delete_konsentrasi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MahasiswaKonsentrasiDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete mahasiswa konsentrasi",
    }
