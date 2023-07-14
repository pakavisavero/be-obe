from fastapi import Request
from fastapi import Depends, status, Header

from controller import moduleGroup
from routes.route import app
from controller.utils import help_filter

from db.session import db, getUsername
from db.database import Session
from db.schemas.moduleGroupSchema import (
    ModuleGroupResponseSchema,
    ModuleGroupCreateSchema,
    ModuleGroupUpdateSchema,
    ModuleGroupDeleteSchema,
)

MODULE_GROUP = "/module-group"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(MODULE_GROUP + "s", response_model=ModuleGroupResponseSchema)
# @check_access_module
async def get_all_module_groups(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = moduleGroup.getAllPagingFiltered(
            db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered module group",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = moduleGroup.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all module group",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(MODULE_GROUP + "/{id}", response_model=ModuleGroupResponseSchema)
# @check_access_module
async def get_module_group(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = moduleGroup.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get module group",
        "data": data,
    }


@app.post(MODULE_GROUP, response_model=ModuleGroupResponseSchema)
# @check_access_module
async def submit_module_group(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: ModuleGroupCreateSchema = None,
):
    username = getUsername(token)

    res = moduleGroup.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit module group",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit module group",
        }


@app.put(MODULE_GROUP, response_model=ModuleGroupResponseSchema)
# @check_access_module
async def update_module_group(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: ModuleGroupUpdateSchema = None,
):
    username = getUsername(token)
    res = moduleGroup.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update module group",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update module group",
        }


@app.delete(MODULE_GROUP)
# @check_access_module
async def delete_module_group(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: ModuleGroupDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete module group",
    }
