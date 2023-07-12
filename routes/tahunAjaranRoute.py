from fastapi import Request
from fastapi import Depends, status, Header

from controller import tahunAjaran
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.schemas.tahunAjaranSchema import (
    TahunAjaranResponseSchema,
    TahunAjaranCreateSchema,
    TahunAjaranUpdateSchema,
    TahunAjaranDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

TAHUN_AJARAN = "/tahun-ajaran"
MODULE_NAME = "Tahun Ajaran"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(TAHUN_AJARAN + "s", response_model=TahunAjaranResponseSchema)
# @check_access_module
async def get_all_tahun_ajaran(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = tahunAjaran.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered tahun ajaran",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = tahunAjaran.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all tahun ajaran",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(TAHUN_AJARAN + "/{id}", response_model=TahunAjaranResponseSchema)
@check_access_module
async def get_tahun_ajaran(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
    request: Request = None,
):
    data = tahunAjaran.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get tahun ajaran",
        "data": data,
    }


@app.post(TAHUN_AJARAN, response_model=TahunAjaranResponseSchema)
@check_access_module
async def submit_tahun_ajaran(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: TahunAjaranCreateSchema = None,
    request: Request = None,
):
    username = getUsername(token)

    res = tahunAjaran.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit tahun ajaran",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit tahun ajaran",
        }


@app.put(TAHUN_AJARAN, response_model=TahunAjaranResponseSchema)
@check_access_module
async def update_tahun_ajaran(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: TahunAjaranUpdateSchema = None,
    request: Request = None,
):
    username = getUsername(token)
    res = tahunAjaran.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update tahun ajaran",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update tahun ajaran",
        }


@app.delete(TAHUN_AJARAN)
async def delete_tahun_ajaran(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: TahunAjaranDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete tahun ajaran",
    }
