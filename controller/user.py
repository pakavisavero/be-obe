from db.models import User, UserRole
from db.database import Session
from db.schemas.userSchema import (
    UserCreateSchema,
    UserUpdateSchema,
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
    data = db.query(User).all()

    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(User)

    data = base_query.all()
    total = base_query.count()

    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str, xtra={}):
    data, total = helper_static_filter(db, User, filtered, offset, xtra)

    return {"data": data, "total": total}


def getAllPagingFilteredSpecialDosen(
    db: Session, offset: int, filtered: dict, token: str, xtra={}
):
    data, total = helper_static_filter(db, UserRole, filtered, offset, xtra)

    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(User).filter_by(id=id).first()

    return data


def getOnlyDosen(db: Session, data: list):
    outputData = []
    for dt in data:
        dosen = db.query(User).filter_by(id=dt.user_id).first()
        outputData.append(dosen)

    return outputData


def create(db: Session, username: str, data: UserCreateSchema):
    try:
        data.created_at = datetime.now()
        data.modified_at = datetime.now()
        data.created_by = username
        data.modified_by = username

        user = User(**data.dict())
        db.add(user)
        db.commit()

        return user

    except Exception as e:
        print(e)
        return False


def update(db: Session, username: str, data: UserUpdateSchema):
    try:
        data.modified_at = datetime.now()
        data.modified_by = username

        user = db.query(User).filter(User.id == data.id).update(dict(data))

        db.commit()

        return user

    except:
        return False


def delete(db: Session, id: int):
    return db.query(User).filter_by(id=id).delete()
