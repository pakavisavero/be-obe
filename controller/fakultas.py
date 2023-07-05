from db.models import Fakultas
from db.database import Session
from db.schemas.fakultasSchema import (
    FakultasCreateSchema,
    FakultasUpdateSchema,
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
    data = db.query(Fakultas).all()

    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(Fakultas)

    data = base_query.all()
    total = base_query.count()

    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str):
    data, total = helper_static_filter(db, Fakultas, filtered, offset)

    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(Fakultas).filter_by(id=id).first()

    return data


def create(db: Session, username: str, data: FakultasCreateSchema):
    try:
        data.created_at = datetime.now()
        data.modified_at = datetime.now()
        data.created_by = username
        data.modified_by = username

        fakultas = Fakultas(**data.dict())
        db.add(fakultas)
        db.commit()

        return fakultas

    except Exception as e:
        print(e)
        return False


def update(db: Session, username: str, data: FakultasUpdateSchema):
    try:
        data.modified_at = datetime.now()
        data.modified_by = username

        fakultas = db.query(Fakultas).filter(Fakultas.id == data.id).update(dict(data))

        db.commit()

        return fakultas

    except:
        return False


def delete(db: Session, id: int):
    return db.query(Fakultas).filter_by(id=id).delete()
