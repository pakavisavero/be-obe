from db.models import StatusMahasiswa
from db.database import Session
from db.schemas.statusMahasiswaSchema import (
    StatusMahasiswaCreateSchema,
    StatusMahasiswaCreateSchema,
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
    data = db.query(StatusMahasiswa).all()

    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(StatusMahasiswa)

    data = base_query.all()
    total = base_query.count()

    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str):
    data, total = helper_static_filter(db, StatusMahasiswa, filtered, offset)

    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(StatusMahasiswa).filter_by(id=id).first()

    return data


def create(db: Session, username: str, data: StatusMahasiswaCreateSchema):
    try:
        data.created_at = datetime.now()
        data.modified_at = datetime.now()
        data.created_by = username
        data.modified_by = username

        statusMhs = StatusMahasiswa(**data.dict())
        db.add(statusMhs)
        db.commit()

        return statusMhs

    except Exception as e:
        print(e)
        return False


def update(db: Session, username: str, data: StatusMahasiswaCreateSchema):
    try:
        data.modified_at = datetime.now()
        data.modified_by = username

        statusMhs = (
            db.query(StatusMahasiswa)
            .filter(StatusMahasiswa.id == data.id)
            .update(dict(data))
        )

        db.commit()

        return statusMhs

    except:
        return False


def delete(db: Session, id: int):
    return db.query(StatusMahasiswa).filter_by(id=id).delete()
