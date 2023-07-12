from fastapi import Request
from fastapi import Depends, status, Header

from controller import mahasiswa
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.schemas.mahasiswaSchema import (
    MahasiswaResponseSchema,
    MahasiswaCreateSchema,
    MahasiswaUpdateSchema,
    MahasiswaDeleteSchema,
)

MAHASISWA = "/mahasiswa"
MODULE_NAME = "Mahasiswa"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(MAHASISWA + "s", response_model=MahasiswaResponseSchema)
@check_access_module
async def get_all_mahasiswa(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
    module_access=MODULE_NAME,
):
    try:
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

    except Exception as e:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error retrieve mahasiswa",
        }


@app.get(MAHASISWA + "/{id}", response_model=MahasiswaResponseSchema)
@check_access_module
async def get_mahasiswa(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
    request: Request = None,
    module_access=MODULE_NAME,
):
    data = mahasiswa.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get mahasiswa",
        "data": data,
    }


@app.post(MAHASISWA + "/raport", response_model=MahasiswaResponseSchema)
@check_access_module
async def get_mahasiswa(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    module_access=MODULE_NAME,
    data: dict = None
):
    pks = []
    if 'pks' in data:
        pks = data['pks']

    mhs = mahasiswa.getByID(db, data['id'], token, pks)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get mahasiswa",
        "data": mhs,
    }

@app.post(MAHASISWA, response_model=MahasiswaResponseSchema)
@check_access_module
async def submit_mahasiswa(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MahasiswaCreateSchema = None,
    request: Request = None,
    module_access=MODULE_NAME,
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


@app.put(MAHASISWA, response_model=MahasiswaResponseSchema)
@check_access_module
async def update_mahasiswa(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MahasiswaUpdateSchema = None,
    request: Request = None,
    module_access=MODULE_NAME,
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


@app.delete(MAHASISWA)
async def delete_mahasiswa(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MahasiswaDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete mahasiswa",
    }
