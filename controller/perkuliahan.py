from db.models import Perkuliahan
from db.database import Session
from db.schemas.perkuliahanSchema import (
    PerkuliahanCreateSchema,
    PerkuliahanUpdateSchema,
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
    data = db.query(Perkuliahan).all()

    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(Perkuliahan)

    data = base_query.all()
    total = base_query.count()

    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str):
    data, total = helper_static_filter(db, Perkuliahan, filtered, offset)

    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(Perkuliahan).filter_by(id=id).first()

    return data


def create(db: Session, username: str, data: PerkuliahanCreateSchema):
    try:
        data.created_at = datetime.now()
        data.modified_at = datetime.now()
        data.created_by = username
        data.modified_by = username

        perkuliahan = Perkuliahan(**data.dict())
        db.add(perkuliahan)
        db.commit()

        return perkuliahan

    except Exception as e:
        print(e)
        return False


def update(db: Session, username: str, data: PerkuliahanUpdateSchema):
    try:
        data.modified_at = datetime.now()
        data.modified_by = username

        perkuliahan = (
            db.query(Perkuliahan).filter(Perkuliahan.id == data.id).update(dict(data))
        )

        db.commit()

        return perkuliahan

    except:
        return False


def delete(db: Session, id: int):
    return db.query(Perkuliahan).filter_by(id=id).delete()
