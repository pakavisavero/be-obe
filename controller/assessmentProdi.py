from db.models import *
from db.database import Session

from .utils import helper_static_filter
from datetime import datetime
import pytz

tz = pytz.timezone("Asia/Jakarta")


def helperRetrieveAssessmentProdi(db, data):
    graph = []
    listSiklus = []

    existCplList = False
    initSiklus = False

    for child in data.children:
        listSiklus.append(child.siklus.name)
        siklus = child.siklus.children

        # Iterasi pada children atau siklus
        for sik in siklus:
            total_values = 0
            mapping = db.query(MappingMahasiswa).filter_by(
                perkuliahan_id=sik.perkuliahan_id).all()

            sum = len(mapping)
            for map in mapping:
                cplMhs = db.query(CplMahasiswa).\
                    filter_by(cpl_id=sik.cpl_id).\
                    filter_by(mapping_mhs_id=map.id).\
                    first()

                if cplMhs:
                    total_values += float(cplMhs.value)

            # Iterasi pada graphic (cpl)
            for cExist in graph:
                name = sik.cpl.name
                if name in cExist:
                    existCplList = True
                    alreadyExistSiklus = False
                    index = 0

                    # Check siklus pada cpl GRAPH
                    for idx, cSiklus in enumerate(cExist[name]):
                        if cSiklus['id'] == child.siklus_id:
                            alreadyExistSiklus = True
                            index = idx

                    if alreadyExistSiklus:
                        cExist[name][index]['sum'] += sum
                        cExist[name][index]['value'] += round(
                            total_values / 25, 2)
                    else:
                        if not initSiklus:
                            cExist[name].append({
                                'id': child.siklus_id,
                                'pk_id': sik.perkuliahan_id,
                                'siklus': child.siklus.name,
                                'sum': sum,
                                'value': round(total_values / 25, 2),
                            })
                            initSiklus = True

                initSiklus = False

            if not existCplList:
                graph.append(
                    {
                        sik.cpl.name: [
                            {
                                'id': child.siklus_id,
                                'pk_id': sik.perkuliahan_id,
                                'siklus': child.siklus.name,
                                'sum': sum,
                                'value': round(total_values / 25, 2),
                            }
                        ],
                    }
                )

            existCplList = False

    setattr(data, 'graph', graph)
    setattr(data, 'listSiklus', listSiklus)


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

    helperRetrieveAssessmentProdi(db, data)

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
