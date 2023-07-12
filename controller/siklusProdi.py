from db.models import *
from db.database import Session

from .utils import helper_static_filter
from datetime import datetime
from routes.cplRoute import logicRetrieveSpecificCPL

import pytz, random

tz = pytz.timezone("Asia/Jakarta")


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


def getAll(db: Session, token: str):
    data = db.query(SiklusProdi).all()

    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(SiklusProdi)

    data = base_query.all()
    total = base_query.count()

    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str):
    data, total = helper_static_filter(db, SiklusProdi, filtered, offset)

    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(SiklusProdi).filter_by(id=id).first()
    children = data.children
    
    for child in children:
        uniqueId = random.randrange(100, 100 * 100)
        pk = child.perkuliahan

        ids = []
        mapping = db.query(MappingCpmkCpl).\
            filter_by(cpl_id=child.cpl_id)\
            .all()

        for map in mapping:
            cpmk = db.query(CPMK).filter_by(id=map.cpmk_id).first()
            pk = db.query(Perkuliahan).filter_by(id=cpmk.perkuliahan_id).first()

            if not pk.id in ids:
                jmlMhs = 0
                total = 0.0
                mappingMhs = (
                    db.query(MappingMahasiswa).filter_by(perkuliahan_id=pk.id).all()
                )
                for mhs in mappingMhs:
                    cplValue = (
                        db.query(CplMahasiswa)
                        .filter_by(cpl_id=child.cpl_id)
                        .filter_by(mapping_mhs_id=mhs.id)
                        .first()
                    )
                    if cplValue:
                        val = cplValue.value
                        jmlMhs += 1
                        total += float(val)

                if jmlMhs == 0:
                    jmlMhs = 1

                uniqueId = random.randrange(100, 100 * 100)
                ids.append(pk.id)

                setattr(pk, 'copyId', uniqueId)
                setattr(pk, 'infoCpl', 'CPL' + str(child.cpl_id))
                setattr(pk, 'infoCplStatement', child.cpl.statement)
                setattr(pk, "total", round(total / jmlMhs, 2))

    return data


def create(db: Session, username: str, data: dict):
    data["created_at"] = datetime.now()
    data["modified_at"] = datetime.now()
    data["created_by"] = username
    data["modified_by"] = username

    children = data["siklus"]
    help_remove_data(data)

    siklusProdi = SiklusProdi(**data)
    db.add(siklusProdi)
    db.commit()
    db.refresh(siklusProdi)

    for child in children:
        cpl = db.query(CPL).filter_by(name=child['infoCpl']).first()

        child = SiklusProdiDetail(**{
            'parent_id': siklusProdi.id,
            'perkuliahan_id': child['id'],
            'cpl_id': cpl.id,
        })

        db.add(child)
        db.commit()

    return siklusProdi


def update(db: Session, username: str, data: dict):
    try:
        data.modified_at = datetime.now()
        data.modified_by = username

        siklusProdi = db.query(SiklusProdi).filter(SiklusProdi.id == data.id).update(data)

        db.commit()

        return siklusProdi

    except:
        return False


def delete(db: Session, id: int):
    return db.query(SiklusProdi).filter_by(id=id).delete()


def help_remove_data(data):
    nameArray = [
        "siklus",
        "option",
    ]

    for a in nameArray:
        if a in data:
            del data[a]
