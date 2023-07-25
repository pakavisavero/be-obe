from db.models import TahunAjaran
from db.database import Session
from db.schemas.tahunAjaranSchema import (
    TahunAjaranCreateSchema,
    TahunAjaranUpdateSchema,
)

from .utils import helper_static_filter, error_handling

from datetime import datetime
import pytz

tz = pytz.timezone("Asia/Jakarta")


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


def getAll(db: Session, token: str):
    data = db.query(TahunAjaran).all()

    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(TahunAjaran)

    data = base_query.all()
    total = base_query.count()

    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str):
    data, total = helper_static_filter(db, TahunAjaran, filtered, offset)

    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(TahunAjaran).filter_by(id=id).first()

    return data


def create(db: Session, username: str, data: dict):
    try:
        data['created_at'] = datetime.now()
        data['modified_at'] = datetime.now()
        data['created_by'] = username
        data['modified_by'] = username

        isActive = db.query(TahunAjaran).filter_by(is_active=True).first()
        data['is_active'] = False if isActive else True

        ta = TahunAjaran(**data)
        db.add(ta)
        db.commit()

        return {
            'status': True,
            'data': ta
        }

    except Exception as e:
        return error_handling(e)


def update(db: Session, username: str, data: dict):
    try:
        if data['is_active']:
            isActive = db.query(TahunAjaran).filter_by(is_active=True).first()
            if isActive:
                raise Exception(
                    {'message': 'Hanya boleh terdapat 1 tahun ajaran aktif!'})

        data['modified_at'] = datetime.now()
        data['modified_by'] = username

        ta = db.query(TahunAjaran).filter(
            TahunAjaran.id == data['id']).update(dict(data))

        db.commit()

        return {
            'status': True,
            'data': ta
        }

    except Exception as e:
        return error_handling(e)


def delete(db: Session, id: int):
    return db.query(TahunAjaran).filter_by(id=id).delete()
