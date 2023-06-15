from fastapi import Request
from fastapi import Depends, status, Header

from controller import prodi
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getCID, getUsername
from db.database import Session
from db.schemas.mappingCpmkCplSchema import (
    MappingCpmkCplResponseSchema,
    MappingCpmkCplCreateSchema,
    MappingCpmkCplUpdateSchema,
    MappingCpmkCplDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

MODULE_NAME = "mapping-cpmk-cpl"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(MODULE_NAME + "s", response_model=MappingCpmkCplResponseSchema)
# @check_access_module
async def get_all_mapping_cpmk_cpl(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = prodi.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered mapping cpmk cpl",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = prodi.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all mapping cpmk cpl",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(MODULE_NAME + "/{id}", response_model=MappingCpmkCplResponseSchema)
# @check_access_module
async def get_mapping_cpmk_cpl(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = prodi.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get mapping cpmk cpl",
        "data": data,
    }


@app.post(MODULE_NAME, response_model=MappingCpmkCplResponseSchema)
# @check_access_module
async def submit_mapping_cpmk_cpl(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MappingCpmkCplCreateSchema = None,
):
    username = getUsername(token)

    res = prodi.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit mapping cpmk cpl",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit mapping cpmk cpl",
        }


@app.put(MODULE_NAME, response_model=MappingCpmkCplResponseSchema)
# @check_access_module
async def update_mapping_cpmk_cpl(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MappingCpmkCplUpdateSchema = None,
):
    username = getUsername(token)
    res = prodi.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update mapping cpmk cpl",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update mapping cpmk cpl",
        }


@app.delete(MODULE_NAME)
# @check_access_module
async def delete_mapping_cpmk_cpl(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: MappingCpmkCplDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete mapping cpmk cpl",
    }
