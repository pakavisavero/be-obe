from fastapi import Request
from fastapi import Depends, status, Header

from controller import prodiStruktural
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getCID, getUsername
from db.database import Session
from db.schemas.prodiStrukturalSchema import (
    ProdiStrukturalResponseSchema,
    ProdiStrukturalCreateSchema,
    ProdiStrukturalUpdateSchema,
    ProdiStrukturalDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

MODULE_NAME = "prodi-struktural"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(MODULE_NAME + "s", response_model=ProdiStrukturalResponseSchema)
# @check_access_module
async def get_all_prodi_struktural(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = prodiStruktural.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered prodi struktural",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = prodiStruktural.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all prodi struktural",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(MODULE_NAME + "/{id}", response_model=ProdiStrukturalResponseSchema)
# @check_access_module
async def get_prodi_struktural(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = prodiStruktural.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get prodi struktural",
        "data": data,
    }


@app.post(MODULE_NAME, response_model=ProdiStrukturalResponseSchema)
# @check_access_module
async def submit_prodi_struktural(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: ProdiStrukturalCreateSchema = None,
):
    username = getUsername(token)

    res = prodiStruktural.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit prodi struktural",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit prodi struktural",
        }


@app.put(MODULE_NAME, response_model=ProdiStrukturalResponseSchema)
# @check_access_module
async def update_prodi_struktural(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: ProdiStrukturalUpdateSchema = None,
):
    username = getUsername(token)
    res = prodiStruktural.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update prodi struktural",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update prodi struktural",
        }


@app.delete(MODULE_NAME)
# @check_access_module
async def delete_prodi_struktural(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: ProdiStrukturalDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete prodi struktural",
    }
