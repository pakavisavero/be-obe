from db.models import PresentasePK
from db.database import Session
from db.schemas.presentasePkSchema import (
    PresentasePkCreateSchema,
    PresentasePkUpdateSchema,
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
    data = db.query(PresentasePK).all()

    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(PresentasePK)

    data = base_query.all()
    total = base_query.count()

    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str):
    data, total = helper_static_filter(db, PresentasePK, filtered, offset)

    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(PresentasePK).filter_by(id=id).first()

    return data


def create(db: Session, username: str, data: PresentasePkCreateSchema):
    try:
        data.created_at = datetime.now()
        data.modified_at = datetime.now()
        data.created_by = username
        data.modified_by = username

        presentasePk = PresentasePK(**data.dict())
        db.add(presentasePk)
        db.commit()

        return presentasePk

    except Exception as e:
        print(e)
        return False


def update(db: Session, username: str, data: PresentasePkUpdateSchema):
    try:
        data.modified_at = datetime.now()
        data.modified_by = username

        presentasePk = (
            db.query(PresentasePK).filter(PresentasePK.id == data.id).update(dict(data))
        )

        db.commit()

        return presentasePk

    except:
        return False


def delete(db: Session, id: int):
    return db.query(PresentasePK).filter_by(id=id).delete()
