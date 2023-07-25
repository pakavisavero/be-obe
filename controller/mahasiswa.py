from db.models import *
from db.database import Session
from db.schemas.mahasiswaSchema import (
    MahasiswaCreateSchema,
    MahasiswaUpdateSchema,
)

from .utils import helper_static_filter, error_handling
from datetime import datetime
import pytz

tz = pytz.timezone("Asia/Jakarta")


def helperRetrieveMahasiswa(db, data):
    for dt in data:
        doswal = db.query(MahasiswaDoswal).filter_by(
            mahasiswa_id=dt.id).first()
        if doswal:
            dosen = db.query(User).filter_by(id=doswal.dosen_id).first()
            setattr(dt, "doswal", dosen)

        perkuliahan = []
        mapping = db.query(MappingMahasiswa).filter_by(
            mahasiswa_id=dt.id).all()
        for map in mapping:
            mata_kuliah = map.perkuliahan.mataKuliah
            perkuliahan.append(
                {
                    "id": map.perkuliahan.id,
                    "mata_kuliah": mata_kuliah.kode_mk
                    + " - "
                    + mata_kuliah.mata_kuliah,
                    "kelas": map.perkuliahan.kelas,
                    "semester": map.perkuliahan.semester,
                    "tahun_ajaran": map.perkuliahan.tahunAjaran.tahun_ajaran,
                }
            )

        setattr(dt, "perkuliahan", perkuliahan)


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


def getByID(db: Session, id: int, token: str, pks=[]):
    if len(pks) > 0:
        pks = [int(pk) for pk in pks.split(",")]

    data = db.query(Mahasiswa).filter_by(id=id).first()
    mapping = db.query(MappingMahasiswa).filter_by(mahasiswa_id=id).all()

    dataRaportCpl = []
    raportCpl = []
    labels = []

    listOfCpl = db.query(CPL).filter_by(prodi_id=8).all()

    for x in listOfCpl:
        labels.append(x.name)
        raportCpl.append({
            'name': x.name,
            'value': [],
            'rerata': [],
        })

    for map in mapping:
        cpl = db.query(CplMahasiswa).filter_by(mapping_mhs_id=map.id).all()
        for cp in cpl:
            for raport in raportCpl:
                if raport['name'] == cp.cpl.name:
                    if len(pks) > 0:
                        if map.perkuliahan_id in pks:
                            raport['value'].append(round(float(cp.value), 2))
                    else:
                        raport['value'].append(round(float(cp.value), 2))

    cplAll = db.query(CplMahasiswa).all()
    for cp in cplAll:
        for raport in raportCpl:
            if raport['name'] == cp.cpl.name:
                raport['rerata'].append(round(float(cp.value), 2))

    for r in raportCpl:
        value = sum(r['value']) / (len(r['value']) if len(r['value']) else 1)
        rerata = sum(r['rerata']) / (len(r['rerata'])
                                     if len(r['rerata']) else 1)
        minVal = min(r['rerata']) if len(r['rerata']) > 0 else 0
        maxVal = max(r['rerata']) if len(r['rerata']) > 0 else 0

        dataRaportCpl.append([value, rerata, minVal, maxVal])

    setattr(data, 'raportCpl', dataRaportCpl)
    setattr(data, 'labels', labels)
    helperRetrieveMahasiswa(db, [data])
    return data


def create(db: Session, username: str, data: dict):
    try:
        doswal_id = data['doswal_id']
        exist = db.query(Mahasiswa).filter_by(nim=data['nim']).first()

        help_remove_data(data)
        if not exist:
            data['created_at'] = datetime.now()
            data['modified_at'] = datetime.now()
            data['created_by'] = username
            data['modified_by'] = username
            data['full_name'] = data['full_name'].lower().title().strip()

            mahasiswa = Mahasiswa(**data)
            db.add(mahasiswa)
            db.commit()
            db.refresh(mahasiswa)

            md = MahasiswaDoswal(**{
                'mahasiswa_id': mahasiswa.id,
                'dosen_id': doswal_id,
                "angkatan": "20" + str(data['nim'])[6:8],
            })
            db.add(md)
            db.commit()

            return {
                'status': True,
                'data': mahasiswa
            }

        else:
            raise Exception({'message': 'nim mahasiswa already taken!'})

    except Exception as e:
        return error_handling(e)


def update(db: Session, username: str, data: dict):
    try:
        doswal_id = data['doswal_id']
        exist = db.query(Mahasiswa).filter_by(nim=data['nim']).first()

        help_remove_data(data)
        if (not exist) or (exist.id == data['id']):
            data['modified_at'] = datetime.now()
            data['modified_by'] = username

            mahasiswa = (
                db.query(Mahasiswa).filter(
                    Mahasiswa.id == data['id']).update({
                        'nim': data['nim'],
                        'full_name': data['full_name'],
                        'prodi_id': data['prodi_id'],
                    })
            )

            db.commit()

            base_doswal = db.query(MahasiswaDoswal).filter_by(
                dosen_id=doswal_id, mahasiswa_id=data['id'])
            args = {
                'dosen_id': doswal_id,
                "angkatan": "20" + str(data['nim'])[6:8],
            }

            doswal = base_doswal.first()
            if doswal:
                base_doswal.update(args)
                db.commit()

            else:
                args['mahasiswa_id'] = data.id
                md = MahasiswaDoswal(**args)
                db.add(md)
                db.commit()

            return {
                'status': True,
                'data': mahasiswa
            }

        else:
            raise Exception({'message': 'nim mahasiswa already taken!'})

    except Exception as e:
        return error_handling(e)


def delete(db: Session, id: int):
    return db.query(Mahasiswa).filter_by(id=id).delete()


def help_remove_data(data):
    nameArray = [
        "prodi_id_name",
        "doswal_id_name",
        "doswal_id",
        "status_mhs_id_name"
    ]

    for a in nameArray:
        if a in data:
            del data[a]
