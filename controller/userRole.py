from db.models import UserRole
from db.database import Session
from db.schemas.userRoleSchema import (
    UserRoleCreateSchema,
    UserRoleUpdateSchema,
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
    data = db.query(UserRole).all()

    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(UserRole)

    data = base_query.all()
    total = base_query.count()

    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str):
    data, total = helper_static_filter(db, UserRole, filtered, offset)

    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(UserRole).filter_by(id=id).first()

    return data


def create(db: Session, username: str, data: UserRoleCreateSchema):
    try:
        data.created_at = datetime.now()
        data.modified_at = datetime.now()
        data.created_by = username
        data.modified_by = username

        userRole = UserRole(**data.dict())
        db.add(userRole)
        db.commit()

        return userRole

    except Exception as e:
        print(e)
        return False


def update(db: Session, username: str, data: UserRoleUpdateSchema):
    try:
        data.modified_at = datetime.now()
        data.modified_by = username

        userRole = db.query(UserRole).filter(UserRole.id == data.id).update(dict(data))

        db.commit()

        return userRole

    except:
        return False


def delete(db: Session, id: int):
    return db.query(UserRole).filter_by(id=id).delete()
