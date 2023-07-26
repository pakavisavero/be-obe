from db.models import AssessmentProdi, AssessmentProdiDetail
from db.database import Session

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
    data = db.query(AssessmentProdi).all()

    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(AssessmentProdi)

    data = base_query.all()
    total = base_query.count()

    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str):
    data, total = helper_static_filter(db, AssessmentProdi, filtered, offset)

    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(AssessmentProdi).filter_by(id=id).first()

    return data


def create(db: Session, username: str, data: dict):
    data["created_at"] = datetime.now()
    data["modified_at"] = datetime.now()
    data["created_by"] = username
    data["modified_by"] = username

    children = data["siklus"]
    help_remove_data(data)

    ap = AssessmentProdi(**data)
    db.add(ap)
    db.commit()
    db.refresh(ap)

    for child in children:
        child = AssessmentProdiDetail(**{
            'parent_id': ap.id,
            'siklus_id': child,
        })

        db.add(child)
        db.commit()

    return ap


def update(db: Session, username: str, data: dict):
    try:
        data.modified_at = datetime.now()
        data.modified_by = username

        assessmentProdi = db.query(AssessmentProdi).filter(
            AssessmentProdi.id == data.id).update(data)

        db.commit()

        return assessmentProdi

    except:
        return False


def delete(db: Session, id: int):
    return db.query(AssessmentProdi).filter_by(id=id).delete()


def help_remove_data(data):
    nameArray = [
        "data",
        "siklus",
    ]

    for a in nameArray:
        if a in data:
            del data[a]
