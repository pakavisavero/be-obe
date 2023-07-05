from fastapi import Request
from fastapi import Depends, status, Header

from controller import mataKuliah
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.schemas.mataKuliahSchema import (
    MataKuliahResponseSchema,
    MataKuliahCreateSchema,
    MataKuliahUpdateSchema,
    MataKuliahDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

MATA_KULIAH = "/mata-kuliah"
MODULE_NAME = "Mata Kuliah"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(MATA_KULIAH + "s", response_model=MataKuliahResponseSchema)
@check_access_module
async def get_all_mata_kuliah(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
    module_access=MODULE_NAME,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = mataKuliah.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered mata kuliah",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = mataKuliah.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all mata kuliah",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(MATA_KULIAH + "/{id}", response_model=MataKuliahResponseSchema)
@check_access_module
async def get_mata_kuliah(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
    request: Request = None,
    module_access=MODULE_NAME,
):
    data = mataKuliah.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get mata kuliah",
        "data": data,
    }


@app.post(MATA_KULIAH, response_model=MataKuliahResponseSchema)
@check_access_module
async def submit_mata_kuliah(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MataKuliahCreateSchema = None,
    request: Request = None,
    module_access=MODULE_NAME,
):
    username = getUsername(token)

    res = mataKuliah.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit mata kuliah",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit mata kuliah",
        }


@app.put(MATA_KULIAH, response_model=MataKuliahResponseSchema)
@check_access_module
async def update_mata_kuliah(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MataKuliahUpdateSchema = None,
    request: Request = None,
    module_access=MODULE_NAME,
):
    username = getUsername(token)
    res = mataKuliah.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update mata kuliah",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update mata kuliah",
        }


@app.delete(MATA_KULIAH)
async def delete_mata_kuliah(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    data: MataKuliahDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete mata kuliah",
    }
