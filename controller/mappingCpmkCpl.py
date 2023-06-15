from db.models import MappingCpmkCpl
from db.database import Session
from db.schemas.mappingCpmkCplSchema import (
    MappingCpmkCplCreateSchema,
    MappingCpmkCplUpdateSchema,
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
    data = db.query(MappingCpmkCpl).all()

    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(MappingCpmkCpl)

    data = base_query.all()
    total = base_query.count()

    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str):
    data, total = helper_static_filter(db, MappingCpmkCpl, filtered, offset)

    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(MappingCpmkCpl).filter_by(id=id).first()

    return data


def create(db: Session, username: str, data: MappingCpmkCplCreateSchema):
    try:
        data.created_at = datetime.now()
        data.modified_at = datetime.now()
        data.created_by = username
        data.modified_by = username

        mappingCpmkCpl = MappingCpmkCpl(**data.dict())
        db.add(mappingCpmkCpl)
        db.commit()

        return mappingCpmkCpl

    except Exception as e:
        print(e)
        return False


def update(db: Session, username: str, data: MappingCpmkCplUpdateSchema):
    try:
        data.modified_at = datetime.now()
        data.modified_by = username

        mappingCpmkCpl = (
            db.query(MappingCpmkCpl)
            .filter(MappingCpmkCpl.id == data.id)
            .update(dict(data))
        )

        db.commit()

        return mappingCpmkCpl

    except:
        return False


def delete(db: Session, id: int):
    return db.query(MappingCpmkCpl).filter_by(id=id).delete()
