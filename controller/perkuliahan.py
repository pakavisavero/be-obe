import decimal
from db.models import Perkuliahan
from db.database import Session
from db.schemas.perkuliahanSchema import (
    PerkuliahanCreateSchema,
)

from .utils import helper_static_filter, identifyRole
from datetime import datetime
from db.models import *
from controller.utils import decode_token
import pytz
from sqlalchemy import or_
from sqlalchemy import inspect

tz = pytz.timezone("Asia/Jakarta")


def get_nilai_huruf(nilai):
    if nilai >= 80:
        return ["A", 4, "Lulus"]
    elif nilai >= 70:
        return ["B", 3, "Lulus"]
    elif nilai >= 60:
        return ["C", 2, "Lulus"]
    elif nilai >= 51:
        return ["D", 1, "Tidak Lulus"]
    else:
        return ["E", 0, "Tidak Lulus"]


def helperRetrievePerkuliahan(db, data):
    mahasiswa = []
    for dt in data:
        mapping = db.query(MappingMahasiswa).filter_by(perkuliahan_id=dt.id).all()
        # Presentase
        pres = db.query(PresentasePK).filter_by(perkuliahan_id=dt.id).first()
        if pres:
            presDict = {
                c.key: getattr(pres, c.key) for c in inspect(pres).mapper.column_attrs
            }
            setattr(dt, "presentase", presDict)

        for map in mapping:
            filter = {"mapping_mhs_id": map.id}
            mhs = db.query(Mahasiswa).filter_by(id=map.mahasiswa_id).first()
            tugas = db.query(NilaiTugas).filter_by(**filter).all()
            uts = db.query(NilaiUTS).filter_by(**filter).all()
            uas = db.query(NilaiUAS).filter_by(**filter).all()
            praktek = db.query(NilaiPraktek).filter_by(**filter).all()
            nilaiPokok = db.query(NilaiPokok).filter_by(**filter).first()

            for t in tugas:
                setattr(t, "cpmk", t.cpmk)
            for u in uts:
                setattr(u, "cpmk", u.cpmk)
            for p in praktek:
                setattr(p, "cpmk", p.cpmk)
            for u in uas:
                setattr(u, "cpmk", u.cpmk)

            # Kalkulasi Nilai Akhir
            if presDict:
                try:
                    n_tugas = (
                        (decimal.Decimal(presDict["nilai_tugas"].replace("%", "")))
                        * nilaiPokok.nilai_tugas
                        / 100
                    )
                    n_uts = (
                        (decimal.Decimal(presDict["nilai_uts"].replace("%", "")))
                        * nilaiPokok.nilai_uts
                        / 100
                    )
                    n_uas = (
                        (decimal.Decimal(presDict["nilai_uas"].replace("%", "")))
                        * nilaiPokok.nilai_uas
                        / 100
                    )
                    n_praktek = (
                        (decimal.Decimal(presDict["nilai_praktek"].replace("%", "")))
                        * nilaiPokok.nilai_praktek
                        / 100
                    )

                    nilai_akhir = n_tugas + n_uts + n_uas + n_praktek
                    nilai_akhir_alp = get_nilai_huruf(nilai_akhir)

                    setattr(nilaiPokok, "nilai_akhir", nilai_akhir)
                    setattr(nilaiPokok, "nilai_akhir_huruf", nilai_akhir_alp[0])
                    setattr(nilaiPokok, "nilai_akhir_bobot", nilai_akhir_alp[1])
                    setattr(nilaiPokok, "keterangan", nilai_akhir_alp[2])
                except:
                    pass

            raport = {
                "nilai_pokok": nilaiPokok if nilaiPokok else {},
                "tugas": tugas if tugas else [],
                "uts": uts if uts else [],
                "uas": uas if uas else [],
                "praktek": praktek if praktek else [],
            }

            setattr(mhs, "raport", raport)
            mahasiswa.append(mhs)

        setattr(dt, "mahasiswa", mahasiswa.copy())
        mahasiswa.clear()

        # CPL & CPMK
        listOfCPMK = []
        cpmk = db.query(CPMK).filter_by(perkuliahan_id=dt.id).all()
        for cp in cpmk:
            mapping = db.query(MappingCpmkCpl).filter_by(cpmk_id=cp.id).all()
            temp = {"id": cp.id, "name": cp.name, "statement": cp.statement, "cpl": []}

            for map in mapping:
                cpl = map.cpl
                temp["cpl"].append(
                    {
                        "name": cpl.name,
                        "statement": cpl.statement,
                        "value": str(int(map.value) * 100) + " %",
                    }
                )

            listOfCPMK.append(temp.copy())
            temp.clear()

        setattr(dt, "cpmk", listOfCPMK)


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


def insert_cpl(db: Session, token: str, pk: int, SH_CPMK):
    user = decode_token(token)["fullName"]

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
                    "created_by": user,
                    "modified_by": user,
                }
            )
            db.add(cpl)
            db.commit()

    print("success insert CPL ...")


def insert_cpmk(db: Session, token: str, pk: int, SH_CPMK):
    user = decode_token(token)["fullName"]

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
                    "created_by": user,
                    "modified_by": user,
                }
            )
            db.add(cpmk)
            db.commit()
            db.refresh(cpmk)
            checkCPMK = cpmk

        base = {
            "cpmk_id": checkCPMK.id,
            "is_active": True,
            "created_by": user,
            "modified_by": user,
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


def insert_nilai(db: Session, token: str, pk: int, SHEET, Schema, param):
    user = decode_token(token)["fullName"]

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
                        data = Schema(
                            **{
                                "mapping_mhs_id": checkMap.id,
                                "cpmk_id": cpmk.id,
                                "nilai_cpmk": pos,
                                "bobot_cpmk": listBobot[x - 4],
                                "is_active": True,
                                "created_by": user,
                                "modified_by": user,
                            }
                        )
                        db.add(data)
                        db.commit()

                    else:
                        print("Gagal sampe sini ../")

            if param == "tugas":
                nilaiPokok = NilaiPokok(
                    **{
                        "mapping_mhs_id": checkMap.id,
                        "nilai_tugas": row[3],
                        "created_by": user,
                        "modified_by": user,
                    }
                )
                db.add(nilaiPokok)
                db.commit()

            else:
                nilaiPokok = (
                    db.query(NilaiPokok).filter_by(mapping_mhs_id=checkMap.id).first()
                )
                setattr(nilaiPokok, "nilai_" + param, row[3])
                db.commit()

        idx += 1

    print("success insert nilai {} ...".format(param))
