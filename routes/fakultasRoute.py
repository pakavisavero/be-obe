from fastapi import Request
from fastapi import Depends, status, Header

from controller import fakultas
from routes.route import app
from controller.utils import help_filter

from db.session import db, getUsername
from db.database import Session
from db.schemas.fakultasSchema import (
    FakultasResponseSchema,
    FakultasCreateSchema,
    FakultasUpdateSchema,
    FakultasDeleteSchema,
)


FAKULTAS = "/fakultas"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(FAKULTAS + "es", response_model=FakultasResponseSchema)
# @check_access_module
async def get_all_fakultas(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = fakultas.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered fakultas",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = fakultas.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all fakultas",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(FAKULTAS + "/{id}", response_model=FakultasResponseSchema)
# @check_access_module
async def get_fakultas(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = fakultas.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get fakultas",
        "data": data,
    }


@app.post(FAKULTAS, response_model=FakultasResponseSchema)
# @check_access_module
async def submit_fakultas(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: FakultasCreateSchema = None,
):
    username = getUsername(token)

    res = fakultas.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit fakultas",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit fakultas",
        }


@app.put(FAKULTAS, response_model=FakultasResponseSchema)
# @check_access_module
async def update_fakultas(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: FakultasUpdateSchema = None,
):
    username = getUsername(token)
    res = fakultas.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update fakultas",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update fakultas",
        }


@app.delete(FAKULTAS)
# @check_access_module
async def delete_fakultas(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: FakultasDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete fakultas",
    }
