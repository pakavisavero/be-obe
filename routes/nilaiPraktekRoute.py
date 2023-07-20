from fastapi import Request
from fastapi import Depends, status, Header

from controller import nilaiPraktek
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.schemas.nilaiPraktekSchema import (
    NilaiPraktekResponseSchema,
    NilaiPraktekCreateSchema,
    NilaiPraktekUpdateSchema,
    NilaiPraktekDeleteSchema,
)


NILAI_PRAKTEK = "/api/nilai-praktek"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(NILAI_PRAKTEK + "s", response_model=NilaiPraktekResponseSchema)
# @check_access_module
async def get_all_nilai_praktek(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = nilaiPraktek.getAllPagingFiltered(
            db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered nilai praktek",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = nilaiPraktek.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all nilai praktek",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(NILAI_PRAKTEK + "/{id}", response_model=NilaiPraktekResponseSchema)
# @check_access_module
async def get_nilai_praktek(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = nilaiPraktek.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get nilai praktek",
        "data": data,
    }


@app.post(NILAI_PRAKTEK, response_model=NilaiPraktekResponseSchema)
# @check_access_module
async def submit_nilai_praktek(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: NilaiPraktekCreateSchema = None,
):
    username = getUsername(token)

    res = nilaiPraktek.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit nilai praktek",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit nilai praktek",
        }


@app.put(NILAI_PRAKTEK, response_model=NilaiPraktekResponseSchema)
# @check_access_module
async def update_nilai_praktek(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: NilaiPraktekUpdateSchema = None,
):
    username = getUsername(token)
    res = nilaiPraktek.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update nilai praktek",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update nilai praktek",
        }


@app.delete(NILAI_PRAKTEK)
# @check_access_module
async def delete_nilai_praktek(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: NilaiPraktekDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete nilai praktek",
    }
