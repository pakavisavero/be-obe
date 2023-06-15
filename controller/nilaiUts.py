from db.models import NilaiUTS
from db.database import Session
from db.schemas.nilaiUtsSchema import (
    NilaiUtsCreateSchema,
    NilaiUtsUpdateSchema,
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
    data = db.query(NilaiUTS).all()

    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(NilaiUTS)

    data = base_query.all()
    total = base_query.count()

    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str):
    data, total = helper_static_filter(db, NilaiUTS, filtered, offset)

    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(NilaiUTS).filter_by(id=id).first()

    return data


def create(db: Session, username: str, data: NilaiUtsCreateSchema):
    try:
        data.created_at = datetime.now()
        data.modified_at = datetime.now()
        data.created_by = username
        data.modified_by = username

        nilaiUts = NilaiUTS(**data.dict())
        db.add(nilaiUts)
        db.commit()

        return nilaiUts

    except Exception as e:
        print(e)
        return False


def update(db: Session, username: str, data: NilaiUtsUpdateSchema):
    try:
        data.modified_at = datetime.now()
        data.modified_by = username

        nilaiUts = db.query(NilaiUTS).filter(NilaiUTS.id == data.id).update(dict(data))

        db.commit()

        return nilaiUts

    except:
        return False


def delete(db: Session, id: int):
    return db.query(NilaiUTS).filter_by(id=id).delete()
