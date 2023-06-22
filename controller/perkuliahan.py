from db.models import Perkuliahan
from db.database import Session
from db.schemas.perkuliahanSchema import (
    PerkuliahanCreateSchema,
    PerkuliahanUpdateSchema,
)

from .utils import helper_static_filter, identifyRole
from datetime import datetime
from db.models import *
import pytz
from sqlalchemy import or_
from sqlalchemy.orm import load_only

tz = pytz.timezone("Asia/Jakarta")


def helperRetrievePerkuliahan(db, data):
    mahasiswa = []
    for dt in data:
        mapping = db.query(MappingMahasiswa).filter_by(perkuliahan_id=dt.id).all()
        for map in mapping:
            filter = {"mapping_mhs_id": map.id}
            mhs = db.query(Mahasiswa).filter_by(id=map.mahasiswa_id).first()
            tugas = db.query(NilaiTugas).filter_by(**filter).first()
            uts = db.query(NilaiUTS).filter_by(**filter).first()
            uas = db.query(NilaiUAS).filter_by(**filter).first()
            praktek = db.query(NilaiPraktek).filter_by(**filter).first()

            raport = {
                "tugas": tugas,
                "uts": uts,
                "uas": uas,
                "praktek": praktek,
            }

            setattr(mhs, "raport", raport)
            mahasiswa.append(mhs)

        setattr(dt, "mahasiswa", mahasiswa.copy())
        mahasiswa.clear()

        cpmk = (
            db.query(CPMK)
            .filter_by(perkuliahan_id=dt.id)
            .options(load_only("id"))
            .all()
        )

        idsCpmk = [x.id for x in cpmk]
        idsCpl = (
            db.query(MappingCpmkCpl)
            .filter(MappingCpmkCpl.id.in_(idsCpmk))
            .options(load_only("cpl_id"))
            .distinct(MappingCpmkCpl.cpl_id)
            .all()
        )

        listOfCPl = []
        for cpl in idsCpl:
            qCPl = db.query(CPL).filter_by(id=cpl.cpl_id).first()
            temp = {"name": qCPl.name, "statement": qCPl.statement, "cpmk": []}

            for cpmk in idsCpmk:
                mapping = (
                    db.query(MappingCpmkCpl)
                    .filter_by(cpl_id=cpl.cpl_id)
                    .filter_by(cpmk_id=cpmk)
                    .first()
                )

                if mapping:
                    qCpmk = mapping.cpmk
                    temp["cpmk"].append(
                        {
                            "name": qCpmk.name,
                            "statement": qCpmk.statement,
                        }
                    )

            listOfCPl.append(temp.copy())
            temp.clear()

        setattr(dt, "cpl", listOfCPl)


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


def getAll(db: Session, token: str):
    data = db.query(Perkuliahan).all()

    helperRetrievePerkuliahan(db, data)

    return data


def getAllPaging(db: Session, offset: int, token: str):
    data = db.query(Perkuliahan)
    role = identifyRole(token)

    if role["role"] == "Dosen":
        data = data.filter(
            or_(
                Perkuliahan.dosen_id == role["user_id"],
                Perkuliahan.dosen2_id == role["user_id"],
                Perkuliahan.dosen3_id == role["user_id"],
            )
        ).all()

    else:
        data = data.all()

    total = len(data)
    helperRetrievePerkuliahan(db, data)
    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str):
    xtra = {}
    xtraOr = {}
    role = identifyRole(token)

    if role["role"] == "Dosen":
        xtraOr = or_(
            Perkuliahan.dosen_id == role["user_id"],
            Perkuliahan.dosen2_id == role["user_id"],
            Perkuliahan.dosen3_id == role["user_id"],
        )

    data, total = helper_static_filter(db, Perkuliahan, filtered, offset, xtra, xtraOr)

    helperRetrievePerkuliahan(db, data)
    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(Perkuliahan).filter_by(id=id).first()

    helperRetrievePerkuliahan(db, [data])
    return data


def create(db: Session, username: str, data: PerkuliahanCreateSchema):
    try:
        data.created_at = datetime.now()
        data.modified_at = datetime.now()
        data.created_by = username
        data.modified_by = username

        perkuliahan = Perkuliahan(**data.dict())
        db.add(perkuliahan)
        db.commit()

        return perkuliahan

    except Exception as e:
        print(e)
        return False


def update(db: Session, username: str, data: dict):
    try:
        data["modified_at"] = datetime.now()
        data["modified_by"] = username

        perkuliahan = (
            db.query(Perkuliahan).filter(Perkuliahan.id == data["id"]).update(data)
        )

        db.commit()

        return perkuliahan

    except:
        return False


def delete(db: Session, id: int):
    return db.query(Perkuliahan).filter_by(id=id).delete()


def insert_cpl(db: Session, pk: int, SH_CPMK):
    startCPL = 18
    endCPL = 32
    rowLen = 28
    for row in range(startCPL, endCPL + 1):
        dis = rowLen - len(SH_CPMK[row])
        if dis > 0:
            for _ in range(0, dis):
                SH_CPMK[row].append("")

        chars_to_remove = ["[", "]", "-"]
        sc = set(chars_to_remove)

        name = "".join([c for c in SH_CPMK[row][26] if c not in sc]).strip()
        statement = SH_CPMK[row][27]

        if statement == "":
            break

        checkCPL = db.query(CPL).filter_by(name=name).first()
        if not checkCPL:
            cpl = CPL(
                **{
                    "prodi_id": 8,
                    "name": name,
                    "statement": statement,
                    "is_active": True,
                }
            )
            db.add(cpl)
            db.commit()

    print("success insert CPL ...")


def insert_cpmk(db: Session, pk: int, SH_CPMK):
    startCPMK = 18
    endCPMK = 32
    rowLen = 12

    for row in range(startCPMK, endCPMK + 1):
        dis = rowLen - len(SH_CPMK[row])
        if dis > 0:
            for _ in range(0, dis):
                SH_CPMK[row].append(None)

        name = SH_CPMK[row][1].strip()
        statement = SH_CPMK[row][2]

        if statement == None:
            break

        checkCPMK = db.query(CPMK).filter_by(name=name).first()

        if not checkCPMK:
            cpmk = CPMK(
                **{
                    "perkuliahan_id": pk,
                    "name": name,
                    "statement": statement,
                    "is_active": True,
                }
            )
            db.add(cpmk)
            db.commit()
            db.refresh(cpmk)
            checkCPMK = cpmk

        base = {
            "cpmk_id": checkCPMK.id,
            "is_active": True,
        }

        cpl1 = SH_CPMK[row][3]
        cpl2 = SH_CPMK[row][4]
        cpl3 = SH_CPMK[row][5]
        cpl4 = SH_CPMK[row][6]
        cpl5 = SH_CPMK[row][7]
        cpl6 = SH_CPMK[row][8]
        cpl7 = SH_CPMK[row][9]
        cpl8 = SH_CPMK[row][10]
        cpl9 = SH_CPMK[row][11]
        cpl10 = SH_CPMK[row][12]

        listCPL = [cpl1, cpl2, cpl3, cpl4, cpl5, cpl6, cpl7, cpl8, cpl9, cpl10]

        for id, el in enumerate(listCPL):
            if el is not None:
                cpl = (
                    db.query(CPL)
                    .filter_by(name="CPL" + str(id + 1))
                    .filter_by(prodi_id=8)
                    .first()
                )
                base["cpl_id"] = cpl.id
                base["value"] = el

                checkMap = (
                    db.query(MappingCpmkCpl)
                    .filter_by(cpmk_id=checkCPMK.id)
                    .filter_by(cpmk_id=base["cpl_id"])
                    .first()
                )
                if not checkMap:
                    map = MappingCpmkCpl(**base)
                    db.add(map)
                    db.commit()
                    checkMap = map

    print("success insert CPMK ...")


def insert_nilai(db: Session, pk: int, SHEET, Schema, param):
    rowLen = 17
    listBobot = []
    for a in range(4, rowLen):
        listBobot.append(SHEET[6][a])

    idx = 0
    for row in SHEET:
        if idx >= 7:
            dis = rowLen - len(row)
            if dis > 0:
                for _ in range(0, dis):
                    row.append(None)

            nim = str(row[1]).strip()
            nilai_total = row[3]

            checkMhs = db.query(Mahasiswa).filter_by(nim=nim).first()
            if not checkMhs:
                print("Tidak ada Mahasiswa!")
                break

            checkMap = (
                db.query(MappingMahasiswa)
                .filter_by(mahasiswa_id=checkMhs.id)
                .filter_by(perkuliahan_id=pk)
                .first()
            )

            if not checkMap:
                print("Tidak ada Mapping!")
                break

            for x in range(4, rowLen):
                pos = row[x]
                if pos != 0:
                    cpmk = (
                        db.query(CPMK)
                        .filter_by(perkuliahan_id=pk)
                        .filter_by(name="CPMK" + str(x - 3))
                        .first()
                    )

                    if cpmk:
                        print("sampe sini ../")
                        data = Schema(
                            **{
                                "mapping_mhs_id": checkMap.id,
                                "cpmk_id": cpmk.id,
                                "nilai_" + param: nilai_total,
                                "nilai_cpmk": pos,
                                "bobot_cpmk": listBobot[x - 4],
                                "is_active": True,
                            }
                        )
                        db.add(data)
                        db.commit()

                    else:
                        print("Gagal sampe sini ../")
        idx += 1

    print("success insert nilai {} ...".format(param))
