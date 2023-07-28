from fastapi import Request
from fastapi import Depends, status, Header

from controller import prodi
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.schemas.prodiSchema import (
    ProdiResponseSchema,
    ProdiCreateSchema,
    ProdiUpdateSchema,
    ProdiDeleteSchema,
)

PRODI = "/api/prodi"
MODULE_NAME = "Program Studi"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(PRODI + "s", response_model=ProdiResponseSchema)
# @check_access_module
async def get_all_prodi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
    module_access=MODULE_NAME,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = prodi.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered prodi",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = prodi.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all prodi",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(PRODI + "/{id}", response_model=ProdiResponseSchema)
# @check_access_module
async def get_prodi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
    request: Request = None,
    module_access=MODULE_NAME,
):
    data = prodi.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get prodi",
        "data": data,
    }


@app.post(PRODI, response_model=ProdiResponseSchema)
# @check_access_module
async def submit_prodi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: ProdiCreateSchema = None,
    request: Request = None,
    module_access=MODULE_NAME,
):
    username = getUsername(token)

    res = prodi.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit prodi",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit prodi",
        }


@app.put(PRODI, response_model=ProdiResponseSchema)
# @check_access_module
async def update_prodi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: ProdiUpdateSchema = None,
    request: Request = None,
    module_access=MODULE_NAME,
):
    username = getUsername(token)
    res = prodi.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update prodi",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update prodi",
        }


@app.delete(PRODI)
async def delete_prodi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: ProdiDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete prodi",
    }
