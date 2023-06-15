from db.models import RolePermission
from db.database import Session
from db.schemas.rolePermissionSchema import (
    RolePermissionCreateSchema,
    RolePermissionUpdateSchema,
)

from .utils import helper_static_filter
from datetime import datetime
import pytz

tz = pytz.timezone("Asia/Jakarta")


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


def getAll(db: Session, token: str):
    data = db.query(RolePermission).all()

    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(RolePermission)

    data = base_query.all()
    total = base_query.count()

    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str):
    data, total = helper_static_filter(db, RolePermission, filtered, offset)

    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(RolePermission).filter_by(id=id).first()

    return data


def create(db: Session, username: str, data: RolePermissionCreateSchema):
    try:
        data.created_at = datetime.now()
        data.modified_at = datetime.now()
        data.created_by = username
        data.modified_by = username

        rolePermission = RolePermission(**data.dict())
        db.add(rolePermission)
        db.commit()

        return rolePermission

    except Exception as e:
        print(e)
        return False


def update(db: Session, username: str, data: RolePermissionUpdateSchema):
    try:
        data.modified_at = datetime.now()
        data.modified_by = username

        rolePermission = (
            db.query(RolePermission)
            .filter(RolePermission.id == data.id)
            .update(dict(data))
        )

        db.commit()

        return rolePermission

    except:
        return False


def delete(db: Session, id: int):
    return db.query(RolePermission).filter_by(id=id).delete()
