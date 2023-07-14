from fastapi import Request
from sqlalchemy import or_
from sqlalchemy import inspect
from openpyxl import load_workbook
from jinja2 import Template
from pyvirtualdisplay import Display
from jinja2 import Environment, FileSystemLoader
from starlette.datastructures import URL
from pypdf import PdfMerger

from db.models import *
from db.database import Session
from db.schemas.perkuliahanSchema import (
    PerkuliahanCreateSchema,
)

from controller.utils import decode_token
from datetime import datetime
from .utils import helper_static_filter, identifyRole


import pytz
import pdfkit
import shutil
import os
import decimal


tz = pytz.timezone("Asia/Jakarta")


def get_nilai_huruf(nilai, cpmk=[]):
    init = False
    ketCPMK = "Lulus"
    color = "#92d050"

    for cp in cpmk:
        if not init and float(cp.value) < 60:
            ketCPMK = "Remidi CPMK"
            color = "#ffffcc"
            init = True

        if nilai >= 80:
            return ["A", 4, ketCPMK, color]
        elif nilai >= 70:
            return ["B", 3, ketCPMK, color]
        elif nilai >= 60:
            return ["C", 2, ketCPMK, color]
        elif nilai >= 51:
            return ["D", 1, "Tidak Lulus", '#c9211e']
        else:
            return ["E", 0, "Tidak Lulus", '#c9211e']


def get_nilai_huruf_no_cpmk(nilai):
    if nilai >= 80:
        return ["A", 4]
    elif nilai >= 70:
        return ["B", 3]
    elif nilai >= 60:
        return ["C", 2]
    elif nilai >= 51:
        return ["D", 1]
    else:
        return ["E", 0]


def get_nilai_huruf_no_remidi(nilai):
    if nilai >= 80:
        return "A"
    elif nilai >= 70:
        return "B"
    elif nilai >= 60:
        return "C"
    elif nilai >= 51:
        return "D"
    else:
        return "E"


def get_single_cpl(cpls):
    temp = {}
    bobot = 0
    for cpl in cpls:
        val = round(float(cpl.value), 2)
        if val >= 80:
            bobot = 4
        elif val >= 70:
            bobot = 3
        elif val >= 60:
            bobot = 2
        elif val >= 51:
            bobot = 1

        temp[cpl.cpl.name] = bobot
        bobot = 0

    return temp


def get_single_cpmk(cpmk):
    temp = {}
    bobot = 0
    for cp in cpmk:
        value = 0
        if cp.value and cp.value != '':
            value = cp.value
        else:
            value = 0

        val = round(float(value), 2)
        if val >= 80:
            bobot = 4
        elif val >= 70:
            bobot = 3
        elif val >= 60:
            bobot = 2
        elif val >= 51:
            bobot = 1

        temp[cp.cpmk.name] = {
            'nilai': val,
            'bobot': bobot,
        }

        bobot = 0

    return temp


def helperRetrievePerkuliahan(db, data):
    mahasiswa = []
    try:
        for dt in data:
            mapping = db.query(MappingMahasiswa).filter_by(
                perkuliahan_id=dt.id).all()
            # Presentase
            pres = db.query(PresentasePK).filter_by(
                perkuliahan_id=dt.id).first()
            if pres:
                presDict = {
                    c.key: getattr(pres, c.key)
                    for c in inspect(pres).mapper.column_attrs
                }
                setattr(dt, "presentase", presDict)

            for map in mapping:
                filter = {"mapping_mhs_id": map.id}
                mhs = db.query(Mahasiswa).filter_by(
                    id=map.mahasiswa_id).first()
                tugas = db.query(NilaiTugas).filter_by(**filter).all()
                uts = db.query(NilaiUTS).filter_by(**filter).all()
                uas = db.query(NilaiUAS).filter_by(**filter).all()
                praktek = db.query(NilaiPraktek).filter_by(**filter).all()
                nilaiPokok = db.query(NilaiPokok).filter_by(**filter).first()

                cpmkMahasiswa = db.query(
                    CpmkMahasiswa).filter_by(**filter).all()
                cplMahasiswa = db.query(CplMahasiswa).filter_by(**filter).all()

                for t in tugas:
                    setattr(t, "cpmk", t.cpmk)
                for u in uts:
                    setattr(u, "cpmk", u.cpmk)
                for p in praktek:
                    setattr(p, "cpmk", p.cpmk)
                for u in uas:
                    setattr(u, "cpmk", u.cpmk)
                for cpmk in cpmkMahasiswa:
                    setattr(cpmk, "cpmk", cpmk.cpmk)
                for cpl in cplMahasiswa:
                    setattr(cpl, "cpl", cpl.cpl)

                # Kalkulasi Nilai Akhir
                if presDict:
                    try:
                        n_tugas = (
                            (decimal.Decimal(
                                presDict["nilai_tugas"].replace("%", "")))
                            * nilaiPokok.nilai_tugas
                            / 100
                        )
                        n_uts = (
                            (decimal.Decimal(
                                presDict["nilai_uts"].replace("%", "")))
                            * nilaiPokok.nilai_uts
                            / 100
                        )
                        n_uas = (
                            (decimal.Decimal(
                                presDict["nilai_uas"].replace("%", "")))
                            * nilaiPokok.nilai_uas
                            / 100
                        )
                        n_praktek = (
                            (
                                decimal.Decimal(
                                    presDict["nilai_praktek"].replace("%", "")
                                )
                            )
                            * nilaiPokok.nilai_praktek
                            / 100
                        )

                        nilai_akhir = n_tugas + n_uts + n_uas + n_praktek
                        nilai_akhir_alp = get_nilai_huruf(
                            nilai_akhir, cpmkMahasiswa)

                        setattr(nilaiPokok, "nilai_akhir", nilai_akhir)
                        setattr(nilaiPokok, "nilai_akhir_huruf",
                                nilai_akhir_alp[0])
                        setattr(nilaiPokok, "nilai_akhir_bobot",
                                nilai_akhir_alp[1])
                        setattr(nilaiPokok, "keterangan", nilai_akhir_alp[2])
                    except:
                        pass

                raport = {
                    "nilai_pokok": nilaiPokok if nilaiPokok else {},
                    "tugas": tugas if tugas else [],
                    "uts": uts if uts else [],
                    "uas": uas if uas else [],
                    "praktek": praktek if praktek else [],
                    "cpmkMhs": cpmkMahasiswa if cpmkMahasiswa else [],
                    "cplMhs": cplMahasiswa if cplMahasiswa else [],
                }

                setattr(mhs, "raport", raport)
                mahasiswa.append(mhs)

            setattr(dt, "mahasiswa", mahasiswa.copy())
            mahasiswa.clear()

            # CPL & CPMK
            listOfCPMK = []
            cpmk = db.query(CPMK).filter_by(perkuliahan_id=dt.id).all()
            for cp in cpmk:
                mapping = db.query(MappingCpmkCpl).filter_by(
                    cpmk_id=cp.id).all()
                temp = {
                    "id": cp.id,
                    "name": cp.name,
                    "statement": cp.statement,
                    "cpl": [],
                }

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

            # Evaluasi
            listEvaluasi = []
            for cp in listOfCPMK:
                evaluasi = db.query(Evaluasi).filter_by(
                    cpmk_id=cp["id"]).first()
                if evaluasi:
                    setattr(evaluasi, "cpmk", evaluasi.cpmk)
                    listEvaluasi.append(evaluasi)

            if len(listEvaluasi) > 0:
                setattr(dt, "evaluasi", listEvaluasi)

            evaluasiMain = (
                db.query(EvaluasiMain).filter_by(perkuliahan_id=dt.id).first()
            )
            if evaluasiMain:
                evalMainDict = {
                    c.key: getattr(evaluasiMain, c.key)
                    for c in inspect(evaluasiMain).mapper.column_attrs
                }
                setattr(dt, "evaluasiMain", evalMainDict)
    except:
        pass


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

    data, total = helper_static_filter(
        db, Perkuliahan, filtered, offset, xtra, xtraOr)

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
            db.query(Perkuliahan).filter(
                Perkuliahan.id == data["id"]).update(data)
        )

        db.commit()

        return perkuliahan

    except:
        return False


def delete(db: Session, id: int):
    return db.query(Perkuliahan).filter_by(id=id).delete()


def insertCpl(db: Session, token: str, pk: int, SH_CPMK):
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
            continue

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


def insertCpmk(db: Session, token: str, pk: int, SH_CPMK):
    user = decode_token(token)["fullName"]

    startCPMK = 18
    endCPMK = 32
    rowLen = 12

    for row in range(startCPMK, endCPMK + 1):
        dis = rowLen - len(SH_CPMK[row])
        if dis > 0:
            for _ in range(0, dis):
                SH_CPMK[row].append(None)

        name = SH_CPMK[row][1]
        statement = SH_CPMK[row][2]

        if (
            name == None or
            statement == None
        ):
            continue

        checkCPMK = (
            db.query(CPMK).filter_by(name=name).filter_by(
                perkuliahan_id=pk).first()
        )

        if not checkCPMK:
            cpmk = CPMK(
                **{
                    "perkuliahan_id": pk,
                    "name": name.strip(),
                    "statement": statement.strip(),
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


def insertNilai(db: Session, token: str, pk: int, SHEET, Schema, param):
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
                # print("Tidak ada Mahasiswa!")
                continue

            checkMap = (
                db.query(MappingMahasiswa)
                .filter_by(mahasiswa_id=checkMhs.id)
                .filter_by(perkuliahan_id=pk)
                .first()
            )

            if not checkMap:
                # print("Tidak ada Mapping!")
                continue

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
                    db.query(NilaiPokok).filter_by(
                        mapping_mhs_id=checkMap.id).first()
                )
                setattr(nilaiPokok, "nilai_" + param, row[3])
                db.commit()

        idx += 1

    print("success insert nilai {} ...".format(param))


def insertCPLMahasiswa(db: Session, token: str, pk: int, SH_CPL_MHS):
    user = decode_token(token)["fullName"]
    start = 7
    end = 250
    length = 15

    for row in range(start, end):
        dis = length - len(SH_CPL_MHS[row])
        if dis > 0:
            for _ in range(0, dis):
                SH_CPL_MHS[row].append("")

        nim = str(SH_CPL_MHS[row][1])
        if nim != "":
            mhsExist = db.query(Mahasiswa).filter_by(nim=nim.strip()).first()
            if mhsExist:
                mapping = (
                    db.query(MappingMahasiswa)
                    .filter_by(perkuliahan_id=pk)
                    .filter_by(mahasiswa_id=mhsExist.id)
                    .first()
                )
                if mapping:
                    for col in range(4, length):
                        if SH_CPL_MHS[row][col] != "":
                            cplName = str(SH_CPL_MHS[5][col])
                            if cplName != "":
                                cpl = (
                                    db.query(CPL)
                                    .filter_by(name=(cplName.strip()))
                                    .first()
                                )
                                cplMhs = CplMahasiswa(
                                    **{
                                        "mapping_mhs_id": mapping.id,
                                        "cpl_id": cpl.id,
                                        "value": SH_CPL_MHS[row][col],
                                        "created_by": user,
                                        "modified_by": user,
                                    }
                                )
                                db.add(cplMhs)
                                db.commit()
            else:
                print("Mahasiswa row {} tidak terdaftar!".format(row))

    print("success insert CPL Mahasiswa ...")


def insertCPMKMahasiswa(db: Session, token: str, pk: int, SH_CPMK_MHS):
    user = decode_token(token)["fullName"]
    start = 7
    end = 250
    length = 40

    for row in range(start, end):
        dis = length - len(SH_CPMK_MHS[row])
        if dis > 0:
            for _ in range(0, dis):
                SH_CPMK_MHS[row].append("")

        nim = str(SH_CPMK_MHS[row][0])
        if nim != "" and nim != None:
            mhsExist = db.query(Mahasiswa).filter_by(nim=nim.strip()).first()
            if mhsExist:
                mapping = (
                    db.query(MappingMahasiswa)
                    .filter_by(perkuliahan_id=pk)
                    .filter_by(mahasiswa_id=mhsExist.id)
                    .first()
                )
                if mapping:
                    for col in range(12, length, 2):
                        if SH_CPMK_MHS[6][col] != "":
                            cpmkName = str(SH_CPMK_MHS[6][col])
                            if cpmkName != "":
                                cpmk = (
                                    db.query(CPMK)
                                    .filter_by(name=cpmkName.strip())
                                    .filter_by(perkuliahan_id=pk)
                                    .first()
                                )
                                cpmkMhs = CpmkMahasiswa(
                                    **{
                                        "mapping_mhs_id": mapping.id,
                                        "cpmk_id": cpmk.id,
                                        "value": SH_CPMK_MHS[row][col],
                                        "created_by": user,
                                        "modified_by": user,
                                    }
                                )

                                db.add(cpmkMhs)
                                db.commit()

                            else:
                                print("stop ...")
                                break

            else:
                pass
                # print("Mahasiswa row {} tidak terdaftar!".format(row))

    print("success insert CPMK Mahasiswa ...")


def insertEvaluasi(db: Session, token: str, pk: int, SH_EVALUASI):
    user = decode_token(token)["fullName"]

    startEvaluasi = 7
    endEvaluasi = 20
    rerataMain = SH_EVALUASI[5][2]
    ambangMain = SH_EVALUASI[5][3]

    evaluasiMain = EvaluasiMain(
        **{
            "perkuliahan_id": pk,
            "rerata": rerataMain,
            "ambang": ambangMain,
        }
    )
    db.add(evaluasiMain)
    db.commit()

    for row in range(startEvaluasi, endEvaluasi):
        dis = 7 - len(SH_EVALUASI[row])
        if dis > 0:
            for _ in range(0, dis):
                SH_EVALUASI[row].append("")

        cpmk = SH_EVALUASI[row][0]
        if cpmk == "":
            continue

        rerata = SH_EVALUASI[row][2]
        ambang = SH_EVALUASI[row][3]
        memenuhi = SH_EVALUASI[row][4]
        analisis = SH_EVALUASI[row][5]
        rencana = SH_EVALUASI[row][6]

        cpmk = (
            db.query(CPMK)
            .filter_by(perkuliahan_id=pk)
            .filter_by(name=cpmk.strip())
            .first()
        )

        if memenuhi == "TIDAK":
            memenuhi = False
        else:
            memenuhi = True

        if cpmk:
            evaluasi = Evaluasi(
                **{
                    "cpmk_id": cpmk.id,
                    "perkuliahan_id": pk,
                    "rerata": rerata,
                    "ambang": ambang,
                    "memenuhi": memenuhi,
                    "analsis": analisis,
                    "rencana": rencana,
                    "created_by": user,
                    "modified_by": user,
                }
            )
            db.add(evaluasi)
            db.commit()

    print("success insert Evaluasi ...")


def getNilaiSiap(db: Session, id: int):
    pk = db.query(Perkuliahan).filter_by(id=id).first()
    matkul = db.query(MataKuliah).filter_by(id=pk.mata_kuliah_id).first()
    presentase = db.query(PresentasePK).filter_by(perkuliahan_id=pk.id).first()
    mapping = db.query(MappingMahasiswa).filter_by(perkuliahan_id=pk.id).all()

    wb = load_workbook("files/siap/template_siap.xlsx")
    sheet = wb["FORM NILAI SIAP"]

    sheet["B1"] = matkul.kode_mk + " - " + matkul.mata_kuliah
    sheet["B2"] = pk.tahunAjaran.tahun_ajaran
    sheet["B3"] = pk.semester
    sheet["B4"] = pk.kelas
    sheet["B5"] = "S1 - Teknik Elektro"

    perTugas = int(presentase.nilai_tugas.replace("%", "")) / 100
    perPraktek = int(presentase.nilai_praktek.replace("%", "")) / 100
    perUts = int(presentase.nilai_uts.replace("%", "")) / 100
    perUas = int(presentase.nilai_uas.replace("%", "")) / 100

    sheet["E6"] = perTugas
    sheet["F6"] = perPraktek
    sheet["G6"] = perUts
    sheet["H6"] = perUas

    row = 8
    for map in mapping:
        mhs = db.query(Mahasiswa).filter_by(id=map.mahasiswa_id).first()
        nilai = db.query(NilaiPokok).filter_by(mapping_mhs_id=map.id).first()

        sheet["A" + str(row)] = mhs.nim
        sheet["B" + str(row)] = mhs.full_name.upper()
        sheet["C" + str(row)] = mhs.semester
        sheet["D" + str(row)] = map.status

        sheet["E" + str(row)] = nilai.nilai_tugas
        sheet["F" + str(row)] = nilai.nilai_praktek
        sheet["G" + str(row)] = nilai.nilai_uts
        sheet["H" + str(row)] = nilai.nilai_uas

        na = (
            (perTugas * float(nilai.nilai_tugas))
            + (perPraktek * float(nilai.nilai_praktek))
            + (perUts * float(nilai.nilai_uts))
            + (perUas * float(nilai.nilai_uas))
        )

        sheet["I" + str(row)] = na
        sheet["J" + str(row)] = get_nilai_huruf_no_cpmk(na)[0]
        sheet["K" + str(row)] = get_nilai_huruf_no_cpmk(na)[1]

        row += 1

    now = datetime.now().strftime("%Y_%m_%d-%I_%M_%S")
    path = "files/siap/SIAP_{}_{}_{}.xlsx".format(
        (matkul.mata_kuliah).upper().replace(
            " ", "_"), pk.semester.lower(), now
    )
    wb.save(path)

    return path


def getJinjaPortofolio(db: Session, request: Request, id: int, template_name: str):
    uri = 'files/template/'
    shutil.copyfile(uri + 'portofolio.html', uri + 'output.html')
    nilais = [
        [
            "Nilai Tugas",
            'nilai_tugas',
            'bobotCpmkTugas',
            'nilai_bobot_tugas',
            'Tugas'
        ],
        [
            "Nilai Praktek",
            'nilai_praktek',
            'bobotCpmkPraktek',
            'nilai_bobot_praktek',
            'Prakt-'
        ],
        [
            "Nilai UTS",
            'nilai_uts',
            'bobotCpmkUts',
            'nilai_bobot_uts',
            ''
        ],
        [
            "Nilai UAS",
            'nilai_uas',
            'bobotCpmkUas',
            'nilai_bobot_uas',
            ''
        ],
    ]

    data = []
    bobotCpmkTugas = []
    bobotCpmkPraktek = []
    bobotCpmkUts = []
    bobotCpmkUas = []
    cpls = []

    pk = db.query(Perkuliahan).filter_by(id=id).first()
    mapping = db.query(MappingMahasiswa).filter_by(perkuliahan_id=id).all()

    mappingCpmk = []
    qCpmks = db.query(CPMK).\
        filter_by(perkuliahan_id=id).\
        all()

    existCpl = []
    for qc in qCpmks:
        qmap = db.query(MappingCpmkCpl).filter_by(cpmk_id=qc.id).first()
        if qmap and qmap.cpl_id not in existCpl:
            existCpl.append(qmap.cpl_id)
            cpls.append(qmap.cpl)

        mappingCpmk.append(qmap)

    for id, q in enumerate(qCpmks):
        bobotTugas = 0
        bobotPraktek = 0
        bobotUts = 0
        bobotUas = 0

        qBobotTugas = db.query(NilaiTugas).filter_by(cpmk_id=q.id).first()
        if qBobotTugas:
            bobotTugas = qBobotTugas.bobot_cpmk

        qBobotPraktek = db.query(NilaiPraktek).filter_by(cpmk_id=q.id).first()
        if qBobotPraktek:
            bobotPraktek = qBobotPraktek.bobot_cpmk

        qBobotUts = db.query(NilaiUTS).filter_by(cpmk_id=q.id).first()
        if qBobotUts:
            bobotUts = qBobotUts.bobot_cpmk

        qBobotUas = db.query(NilaiUAS).filter_by(cpmk_id=q.id).first()
        if qBobotUas:
            bobotUas = qBobotUas.bobot_cpmk

        bobotCpmkTugas.append({
            'id': id + 1,
            'name': q.name,
            'bobot': str(bobotTugas * 100) + '%',
        })

        bobotCpmkPraktek.append({
            'id': id + 1,
            'name': q.name,
            'bobot': str(bobotPraktek * 100) + '%',
        })

        bobotCpmkUts.append({
            'id': id + 1,
            'name': q.name,
            'bobot': str(bobotUts * 100) + '%',
        })
        bobotCpmkUas.append({
            'id': id + 1,
            'name': q.name,
            'bobot': str(bobotUas * 100) + '%',
        })

        bobotTugas = 0
        bobotUts = 0
        bobotUas = 0

    for id, map in enumerate(mapping):
        pokok = db.query(NilaiPokok).filter_by(mapping_mhs_id=map.id).first()

        nilai_bobot_tugas = []
        nilai_bobot_praktek = []
        nilai_bobot_uts = []
        nilai_bobot_uas = []

        nilaiAkhirCpmk = []
        for q in qCpmks:
            cpmkMhs = db.query(CpmkMahasiswa).filter_by(
                mapping_mhs_id=map.id, cpmk_id=q.id).first()
            nilaiAkhirCpmk.append(cpmkMhs)

            filter = {'mapping_mhs_id': map.id, 'cpmk_id': q.id}
            qTugas = db.query(NilaiTugas).filter_by(**filter).first()
            qPraktek = db.query(NilaiPraktek).filter_by(**filter).first()
            qUts = db.query(NilaiUTS).filter_by(**filter).first()
            qUas = db.query(NilaiUAS).filter_by(**filter).first()

            nilai_bobot_tugas.append(
                round(qTugas.nilai_cpmk, 2) if qTugas else 0)
            nilai_bobot_praktek.append(
                round(qPraktek.nilai_cpmk, 2) if qPraktek else 0)
            nilai_bobot_uts.append(round(qUts.nilai_cpmk, 2) if qUts else 0)
            nilai_bobot_uas.append(round(qUas.nilai_cpmk, 2) if qUas else 0)

        pr = db.query(PresentasePK).filter_by(perkuliahan_id=pk.id).first()
        pr_tugas = pr.nilai_tugas
        pr_praktek = pr.nilai_praktek
        pr_uts = pr.nilai_uts
        pr_uas = pr.nilai_uas

        nilai_akhir = round(float(pr_tugas.replace('%', '')) / 100 * float(pokok.nilai_tugas), 2) + \
            round(float(pr_praktek.replace('%', '')) / 100 * float(pokok.nilai_praktek), 2) + \
            round(float(pr_uts.replace('%', '')) / 100 * float(pokok.nilai_uts), 2) + \
            round(float(pr_uas.replace('%', '')) / 100
                  * float(pokok.nilai_uas), 2)

        nilaiAkhirCpl = []
        singleCplMahasiswa = []

        for cpl in cpls:
            cplMhs = db.query(CplMahasiswa).filter_by(
                mapping_mhs_id=map.id, cpl_id=cpl.id).first()
            val = round(float(cplMhs.value), 2)
            nilaiAkhirCpl.append(val)
            singleCplMahasiswa.append(cplMhs)

        division = len(nilaiAkhirCpl)
        if division == 0:
            division = 1

        data.append({
            'no': id + 1,
            'nim': map.mahasiswa.nim,
            'full_name': map.mahasiswa.full_name,
            'semester': map.mahasiswa.semester,
            'status': map.status,
            'nilai_tugas': round(pokok.nilai_tugas, 2),
            'nilai_praktek': round(pokok.nilai_praktek, 2),
            'nilai_uts': round(pokok.nilai_uts, 2),
            'nilai_uas': round(pokok.nilai_uas, 2),
            'nilai_akhir': round(nilai_akhir, 2),
            'nilai_akhir_huruf': get_nilai_huruf(nilai_akhir, mappingCpmk)[0],
            'nilai_bobot': get_nilai_huruf(nilai_akhir, mappingCpmk)[1],
            'keterangan': get_nilai_huruf(nilai_akhir, mappingCpmk)[2],
            'color': get_nilai_huruf(nilai_akhir, mappingCpmk)[3],
            'nilai_bobot_tugas': nilai_bobot_tugas,
            'nilai_bobot_praktek': nilai_bobot_praktek,
            'nilai_bobot_uts': nilai_bobot_uts,
            'nilai_bobot_uas': nilai_bobot_uas,
            'nilai_akhir_cpl': get_nilai_huruf_no_remidi(sum(nilaiAkhirCpl) / division),
            'nilai_single_cpl': get_single_cpl(singleCplMahasiswa),
            'nilai_single_cpmk': get_single_cpmk(nilaiAkhirCpmk)
        })

    pengampu = ""
    if pk.dosen1:
        pengampu += pk.dosen1.full_name + ' / '
    if pk.dosen2:
        pengampu += pk.dosen2.full_name + ' / '
    if pk.dosen3:
        pengampu += pk.dosen3.full_name

    mapping = {}
    for cpmk in qCpmks:
        mapping[cpmk.name] = {}
        map = db.query(MappingCpmkCpl).filter_by(cpmk_id=cpmk.id).all()
        for m in map:
            mapping[cpmk.name][m.cpl.name] = str(
                int(m.value) * 100) + '%'

    evaluasi = {}
    qEval = db.query(Evaluasi).filter_by(perkuliahan_id=pk.id).all()
    for eval in qEval:
        evaluasi[eval.cpmk.name] = {
            'rerata': round(float(eval.rerata if eval.rerata else 0), 2),
            'ambang': str(round(float(eval.ambang if eval.ambang else 0) * 100, 2)) + '%',
            'memenuhi': 'TIDAK' if not eval.memenuhi else "IYA",
            'analsis': eval.analsis,
            'rencana': eval.rencana,
        }

    evaluasiMain = db.query(EvaluasiMain).filter_by(
        perkuliahan_id=pk.id).first()

    setattr(evaluasiMain, 'ambang', str(
        round(float(evaluasiMain.ambang) * 100, 2)) + '%')

    cplProdi = db.query(CPL).filter_by(prodi_id=8).all()
    environment = Environment(loader=FileSystemLoader("files/template/"))
    template = environment.get_template("output.html")
    page = template.render({
        'nilais': nilais,
        'data': data,
        'pk': pk,
        'pengampu': pengampu,
        'cpl_prodis': cplProdi,
        'jm_cpl': len(cplProdi),
        'cpmk_matkul': qCpmks,
        'mapping': mapping,
        'evaluasi': evaluasi,
        'evaluasiMain': evaluasiMain,
        'bobot': {
            'bobotCpmkTugas': bobotCpmkTugas,
            'bobotCpmkPraktek': bobotCpmkPraktek,
            'bobotCpmkUts': bobotCpmkUts,
            'bobotCpmkUas': bobotCpmkUas,
        }
    })

    f = open(uri + 'output.html', "w")
    f.write(page)
    f.close()

    pdfkit.from_file(
        uri + 'output.html',
        uri + 'output.pdf',
        options={"enable-local-file-access": ""},
    )

    os.unlink(uri + 'output.html')

    pdfs = ['files/cpmk/' + template_name,
            'files/template/output.pdf']

    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)

    merger.write(uri + "result.pdf")
    os.unlink(uri + 'output.pdf')

    return uri + 'result.pdf'
