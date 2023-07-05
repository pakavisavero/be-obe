from db.models import MahasiswaKonsentrasi
from db.database import Session
from db.schemas.mahasiswaKonsentrasiSchema import (
    MahasiswaKonsentrasiCreateSchema,
    MahasiswaKonsentrasiUpdateSchema,
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
    data = db.query(MahasiswaKonsentrasi).all()

    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(MahasiswaKonsentrasi)

    data = base_query.all()
    total = base_query.count()

    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str):
    data, total = helper_static_filter(db, MahasiswaKonsentrasi, filtered, offset)

    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(MahasiswaKonsentrasi).filter_by(id=id).first()

    return data


def create(db: Session, username: str, data: MahasiswaKonsentrasiCreateSchema):
    try:
        data.created_at = datetime.now()
        data.modified_at = datetime.now()
        data.created_by = username
        data.modified_by = username

        mhsKonsentrasi = MahasiswaKonsentrasi(**data.dict())
        db.add(mhsKonsentrasi)
        db.commit()

        return mhsKonsentrasi

    except Exception as e:
        print(e)
        return False


def update(db: Session, username: str, data: MahasiswaKonsentrasiUpdateSchema):
    try:
        data.modified_at = datetime.now()
        data.modified_by = username

        mhsKonsentrasi = (
            db.query(MahasiswaKonsentrasi)
            .filter(MahasiswaKonsentrasi.id == data.id)
            .update(dict(data))
        )

        db.commit()

        return mhsKonsentrasi

    except:
        return False


def delete(db: Session, id: int):
    return db.query(MahasiswaKonsentrasi).filter_by(id=id).delete()
