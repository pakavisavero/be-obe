from db.models import *
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
    data["created_at"] = datetime.now()
    data["modified_at"] = datetime.now()
    data["created_by"] = username
    data["modified_by"] = username

    children = data["children"]
    help_remove_data(data)

    am = AssessmentMatkul(**{
        'name': data['name'],
        'description': data['description'],
    })
    
    db.add(am)
    db.commit()
    db.refresh(am)

    for id in children:
        child = AssessmentMatkulDetail(**{
            'parent_id': am.id,
            'perkuliahan_id': int(id),
        })

        db.add(child)
        db.commit()

    return am


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


def help_remove_data(data):
    nameArray = [
        "assessment",
        "option",
        "matkul"
    ]

    for a in nameArray:
        if a in data:
            del data[a]
