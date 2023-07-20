from fastapi import Request
from fastapi import Depends, status, Header

from controller import kurikulum
from routes.route import app
from controller.utils import help_filter

from db.session import db, getUsername
from db.database import Session
from db.schemas.kurikulumSchema import (
    KurikulumResponseSchema,
    KurikulumCreateSchema,
    KurikulumUpdateSchema,
    KurikulumDeleteSchema,
)

KURIKULUM = "/api/kurikulum"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(KURIKULUM + "s", response_model=KurikulumResponseSchema)
# @check_access_module
async def get_all_kurikulum(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = kurikulum.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered kurikulum",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = kurikulum.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all kurikulum",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(KURIKULUM + "/{id}", response_model=KurikulumResponseSchema)
# @check_access_module
async def get_kurikulum(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = kurikulum.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get kurikulum",
        "data": data,
    }


@app.post(KURIKULUM, response_model=KurikulumResponseSchema)
# @check_access_module
async def submit_kurikulum(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: KurikulumCreateSchema = None,
):
    username = getUsername(token)

    res = kurikulum.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit kurikulum",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit kurikulum",
        }


@app.put(KURIKULUM, response_model=KurikulumResponseSchema)
# @check_access_module
async def update_kurikulum(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: KurikulumUpdateSchema = None,
):
    username = getUsername(token)
    res = kurikulum.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update kurikulum",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update kurikulum",
        }


@app.delete(KURIKULUM)
# @check_access_module
async def delete_kurikulum(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: KurikulumDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete kurikulum",
    }
