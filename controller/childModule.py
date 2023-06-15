from db.models import ChildModule
from db.database import Session
from db.schemas.childModuleSchema import (
    ChildModuleCreateSchema,
    ChildModuleUpdateSchema,
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
    data = db.query(ChildModule).all()

    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(ChildModule)

    data = base_query.all()
    total = base_query.count()

    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str):
    data, total = helper_static_filter(db, ChildModule, filtered, offset)

    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(ChildModule).filter_by(id=id).first()

    return data


def create(db: Session, username: str, data: ChildModuleCreateSchema):
    try:
        data.created_at = datetime.now()
        data.modified_at = datetime.now()
        data.created_by = username
        data.modified_by = username

        childModule = ChildModule(**data.dict())
        db.add(childModule)
        db.commit()

        return childModule

    except Exception as e:
        print(e)
        return False


def update(db: Session, username: str, data: ChildModuleUpdateSchema):
    try:
        data.modified_at = datetime.now()
        data.modified_by = username

        childModule = (
            db.query(ChildModule).filter(ChildModule.id == data.id).update(dict(data))
        )

        db.commit()

        return childModule

    except:
        return False


def delete(db: Session, id: int):
    return db.query(ChildModule).filter_by(id=id).delete()
