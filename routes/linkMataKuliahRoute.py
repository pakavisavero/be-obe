from fastapi import Request
from fastapi import Depends, status, Header

from controller import linkMataKuliah
from routes.route import app
from controller.utils import help_filter

from db.session import db, getUsername
from db.database import Session
from db.schemas.linkMataKuliah import (
    LinkMataKuliahResponseSchema,
    LinkMataKuliahCreateSchema,
    LinkMataKuliahUpdateSchema,
    LinkMataKuliahDeleteSchema,
)

LINK_MATA_KULIAH = "/api/link-mata-kuliah"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(LINK_MATA_KULIAH + "s", response_model=LinkMataKuliahResponseSchema)
# @check_access_module
async def get_all_link_mata_kuliah(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = linkMataKuliah.getAllPagingFiltered(
            db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered link mata kuliah",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = linkMataKuliah.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all link mata kuliah",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(LINK_MATA_KULIAH + "/{id}", response_model=LinkMataKuliahResponseSchema)
# @check_access_module
async def get_link_mata_kuliah(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = linkMataKuliah.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get link mata kuliah",
        "data": data,
    }


@app.post(LINK_MATA_KULIAH, response_model=LinkMataKuliahResponseSchema)
# @check_access_module
async def submit_link_mata_kuliah(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: LinkMataKuliahCreateSchema = None,
):
    username = getUsername(token)

    res = linkMataKuliah.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit link mata kuliah",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit link mata kuliah",
        }


@app.put(LINK_MATA_KULIAH, response_model=LinkMataKuliahResponseSchema)
# @check_access_module
async def update_link_mata_kuliah(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: LinkMataKuliahUpdateSchema = None,
):
    username = getUsername(token)
    res = linkMataKuliah.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update link mata kuliah",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update link mata kuliah",
        }


@app.delete(LINK_MATA_KULIAH)
# @check_access_module
async def delete_link_mata_kuliah(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: LinkMataKuliahDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete link mata kuliah",
    }
