from db.models import Mahasiswa, MahasiswaDoswal, User
from db.database import Session
from db.schemas.mahasiswaSchema import (
    MahasiswaCreateSchema,
    MahasiswaUpdateSchema,
)

from .utils import helper_static_filter
from datetime import datetime
import pytz

tz = pytz.timezone("Asia/Jakarta")


def helperRetrieveMahasiswa(db, data):
    for dt in data:
        doswal = db.query(MahasiswaDoswal).filter_by(mahasiswa_id=dt.id).first()
        dosen = db.query(User).filter_by(id=doswal.dosen_id).first()

        if doswal:
            setattr(dt, "doswal", dosen)


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


def getAll(db: Session, token: str):
    data = db.query(Mahasiswa).all()

    helperRetrieveMahasiswa(db, data)
    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(Mahasiswa)

    data = base_query.all()
    total = base_query.count()

    helperRetrieveMahasiswa(db, data)
    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str):
    data, total = helper_static_filter(db, Mahasiswa, filtered, offset)

    helperRetrieveMahasiswa(db, data)
    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(Mahasiswa).filter_by(id=id).first()

    helperRetrieveMahasiswa(db, [data])
    return data


def create(db: Session, username: str, data: MahasiswaCreateSchema):
    try:
        data.created_at = datetime.now()
        data.modified_at = datetime.now()
        data.created_by = username
        data.modified_by = username

        mahasiswa = Mahasiswa(**data.dict())
        db.add(mahasiswa)
        db.commit()

        return mahasiswa

    except Exception as e:
        print(e)
        return False


def update(db: Session, username: str, data: MahasiswaUpdateSchema):
    try:
        data.modified_at = datetime.now()
        data.modified_by = username

        mahasiswa = (
            db.query(Mahasiswa).filter(Mahasiswa.id == data.id).update(dict(data))
        )

        db.commit()

        return mahasiswa

    except:
        return False


def delete(db: Session, id: int):
    return db.query(Mahasiswa).filter_by(id=id).delete()
