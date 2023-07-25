from db.models import Module
from db.database import Session
from db.schemas.moduleSchema import (
    ModuleCreateSchema,
    ModuleUpdateSchema,
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
    data = db.query(Module).all()

    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(Module)

    data = base_query.all()
    total = base_query.count()

    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str):
    data, total = helper_static_filter(db, Module, filtered, offset)

    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(Module).filter_by(id=id).first()

    return data


def create(db: Session, username: str, data: ModuleCreateSchema):
    try:
        data.created_at = datetime.now()
        data.modified_at = datetime.now()
        data.created_by = username
        data.modified_by = username

        module = Module(**data.dict())
        db.add(module)
        db.commit()

        return module

    except Exception as e:
        print(e)
        return False


def update(db: Session, username: str, data: dict):
    try:
        data['modified_at'] = datetime.now()
        data['modified_by'] = username

        help_remove_data(data)

        module = (
            db.query(Module).filter(Module.id == data['id']).update(dict(data))
        )
        db.commit()

        return module

    except:
        return False


def delete(db: Session, id: int):
    return db.query(Module).filter_by(id=id).delete()


def help_remove_data(data):
    nameArray = [
        "moduleGroup",
        "route",
        "module_group_id_name",
    ]

    for a in nameArray:
        if a in data:
            del data[a]
