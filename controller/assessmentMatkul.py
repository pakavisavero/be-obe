from db.models import AssessmentMatkul
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
    data = db.query(AssessmentMatkul).all()

    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(AssessmentMatkul)

    data = base_query.all()
    total = base_query.count()

    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str):
    data, total = helper_static_filter(db, AssessmentMatkul, filtered, offset)

    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(AssessmentMatkul).filter_by(id=id).first()

    return data


def create(db: Session, username: str, data: dict):
    try:
        data["created_at"] = datetime.now()
        data["modified_at"] = datetime.now()
        data["created_by"] = username
        data["modified_by"] = username

        assessmentMatkul = AssessmentMatkul(**data)
        db.add(assessmentMatkul)
        db.commit()

        return assessmentMatkul

    except Exception as e:
        print(e)
        return False


def update(db: Session, username: str, data: dict):
    try:
        data.modified_at = datetime.now()
        data.modified_by = username

        assessmentMatkul = db.query(AssessmentMatkul).filter(AssessmentMatkul.id == data.id).update(data)

        db.commit()

        return assessmentMatkul

    except:
        return False


def delete(db: Session, id: int):
    return db.query(AssessmentMatkul).filter_by(id=id).delete()
