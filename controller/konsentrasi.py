from db.models import Konsentrasi
from db.database import Session
from db.schemas.konsentrasiSchema import (
    KonsentrasiCreateSchema,
    KonsentrasiUpdateSchema,
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
    data = db.query(Konsentrasi).all()

    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(Konsentrasi)

    data = base_query.all()
    total = base_query.count()

    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str):
    data, total = helper_static_filter(db, Konsentrasi, filtered, offset)

    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(Konsentrasi).filter_by(id=id).first()

    return data


def create(db: Session, username: str, data: KonsentrasiCreateSchema):
    try:
        data.created_at = datetime.now()
        data.modified_at = datetime.now()
        data.created_by = username
        data.modified_by = username

        konsentrasi = Konsentrasi(**data.dict())
        db.add(konsentrasi)
        db.commit()

        return konsentrasi

    except Exception as e:
        print(e)
        return False


def update(db: Session, username: str, data: KonsentrasiUpdateSchema):
    try:
        data.modified_at = datetime.now()
        data.modified_by = username

        konsentrasi = (
            db.query(Konsentrasi).filter(Konsentrasi.id == data.id).update(dict(data))
        )

        db.commit()

        return konsentrasi

    except:
        return False


def delete(db: Session, id: int):
    return db.query(Konsentrasi).filter_by(id=id).delete()
