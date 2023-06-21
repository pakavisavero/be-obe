from fastapi import Request, BackgroundTasks
from fastapi import Depends, status, Header

from controller import perkuliahan, mataKuliah, tahunAjaran
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.schemas.perkuliahanSchema import (
    PerkuliahanResponseSchema,
    PerkuliahanCreateSchema,
    PerkuliahanDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.models import *

from openpyxl import load_workbook
from fastapi.responses import FileResponse
from datetime import datetime
from controller.utils import DocStatus


PERKULIAHAN = "/perkuliahan"
MODULE_NAME = "Perkuliahan"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(PERKULIAHAN + "s", response_model=PerkuliahanResponseSchema)
@check_access_module
async def get_all_perkuliahan(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
    module_access=MODULE_NAME,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = perkuliahan.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered perkuliahan",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = perkuliahan.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all perkuliahan",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(PERKULIAHAN + "/{id}", response_model=PerkuliahanResponseSchema)
@check_access_module
async def get_perkuliahan(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
    request: Request = None,
    module_access=MODULE_NAME,
):
    data = perkuliahan.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get perkuliahan",
        "data": data,
    }


@app.post(PERKULIAHAN, response_model=PerkuliahanResponseSchema)
@check_access_module
async def submit_perkuliahan(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: PerkuliahanCreateSchema = None,
    request: Request = None,
    module_access=MODULE_NAME,
):
    username = getUsername(token)

    res = perkuliahan.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit perkuliahan",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit perkuliahan",
        }


@app.put(PERKULIAHAN, response_model=PerkuliahanResponseSchema)
@check_access_module
async def update_perkuliahan(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
    request: Request = None,
    module_access=MODULE_NAME,
):
    username = getUsername(token)
    res = perkuliahan.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update perkuliahan",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update perkuliahan",
        }


@app.delete(PERKULIAHAN)
async def delete_perkuliahan(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: PerkuliahanDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete perkuliahan",
    }


@app.post(PERKULIAHAN + "-upload")
async def upload(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
    request: Request = None,
):
    try:
        data = data["data"]
        thn_ajaran = str(data[0][1]).replace(":", "").strip()
        semester = str(data[1][1]).replace(":", "").strip()

        if semester == "" or thn_ajaran == "":
            raise ValueError(
                "Tidak terdapat semester atau tahun ajaran pada row " + +str(idx)
            )

        headerLen = 10
        idx = 0
        for value in data:
            print(value)
            if idx >= 4 and len(value) > 0:
                dis = headerLen - len(value)
                if dis > 0:
                    for _ in range(0, dis):
                        value.append("")

                matkul = str(value[0]).strip()
                kode = str(value[1]).strip()
                kelas = str(value[2]).strip()
                sks = str((value[3].strip().lower())).replace("sks", "")
                dosen1 = str(value[4]).strip()
                nip_dosen1 = str(value[5]).strip()
                dosen2 = value[6]
                nip_dosen2 = value[7]
                dosen3 = value[8]
                nip_dosen3 = value[9]

                if matkul == "" or kode == "" or nip_dosen1 == "":
                    raise ValueError(
                        "Tidak terdapat mata kuliah, kode atau NIP dosen utama pada row "
                        + +str(idx)
                    )

                isMatkulExist = db.query(MataKuliah).filter_by(kode_mk=kode).first()
                if not isMatkulExist:
                    crMatkul = MataKuliah(
                        **{
                            "kode_mk": kode,
                            "mata_kuliah": matkul.lower().title(),
                            "sks": int(sks),
                            "kurikulum_id": 1,
                            "prodi_id": 8,
                        }
                    )
                    db.add(crMatkul)
                    db.commit()
                    db.refresh(crMatkul)

                    if crMatkul:
                        isMatkulExist = crMatkul
                    else:
                        raise ValueError(
                            "Tidak terdapat mata kuliah yang pada row " + str(idx)
                        )

                ta = db.query(TahunAjaran).filter_by(tahun_ajaran=thn_ajaran).first()
                if not ta:
                    head, _, _ = thn_ajaran.partition("/")
                    ta = TahunAjaran(
                        **{"name": head, "tahun_ajaran": thn_ajaran, "is_active": True}
                    )
                    db.add(ta)
                    db.commit()
                    db.refresh(ta)

                data = {
                    "prodi_id": 8,
                    "mata_kuliah_id": isMatkulExist.id,
                    "kelas": kelas,
                    "tahun_ajaran_id": ta.id,
                    "semester": semester,
                    "is_active": True,
                    "created_by": "Import User",
                    "modified_by": "Import User",
                }

                existDosen1 = db.query(User).filter_by(nip=nip_dosen1).first()
                if not existDosen1:
                    existDosen1 = User(
                        **{
                            "email": dosen1,
                            "nip": nip_dosen1,
                            "full_name": dosen1,
                            "prodi_id": 8,
                        }
                    )
                    db.add(existDosen1)
                    db.commit()
                    db.refresh(existDosen1)

                    crUserRole = UserRole(
                        **{
                            "user_id": existDosen1.id,
                            "role_id": 3,
                        }
                    )
                    db.add(crUserRole)
                    db.commit()
                    db.refresh(crUserRole)

                data["dosen_id"] = existDosen1.id
                data["pj_dosen_id"] = existDosen1.id
                data["doc_status_id"] = int(DocStatus.MENUNGGU_UPLOAD_DPNA.value)

                if nip_dosen2:
                    existDosen2 = db.query(User).filter_by(nip=nip_dosen2).first()
                    if existDosen2:
                        data["dosen2_id"] = existDosen2.id

                if nip_dosen3:
                    existDosen3 = db.query(User).filter_by(nip=nip_dosen3).first()
                    if existDosen3:
                        data["dosen3_id"] = existDosen3.id

                isExistPK = (
                    db.query(Perkuliahan)
                    .filter_by(mata_kuliah_id=data["mata_kuliah_id"])
                    .filter_by(tahun_ajaran_id=ta.id)
                    .filter_by(semester=data["semester"])
                    .filter_by(kelas=data["kelas"])
                    .first()
                )

                if not isExistPK:
                    pk = Perkuliahan(**data)
                    db.add(pk)
                    db.commit()
                    db.refresh(pk)

            idx += 1

        return {
            "code": status.HTTP_200_OK,
            "message": "Success Upload Perkuliahan",
        }

    except Exception as e:
        print(e)
        db.rollback()
        err = str(e.args[0]).split("\n")
        data = {"message": err[errArray(len(err))]}
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": err,
        }


@app.post("/dpna" + "-upload")
async def upload_dpna(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
    request: Request = None,
):
    id = data["id"]
    header = data["data"]

    try:
        c1 = header[0][1]
        if len(c1.split("-")) != 2:
            raise ValueError("Format cell B1 (Kode MK - Matkul) tidak valid!")

        kode_mk = str(c1.split("-")[0]).replace(":", "").strip()
        tahun_ajaran = str(header[1][1]).replace(":", "").strip()
        semester = str(header[2][1]).replace(":", "").strip()
        kelas = str(header[3][1]).replace(":", "").strip()

        checkMatkul = db.query(MataKuliah).filter_by(kode_mk=kode_mk).first()
        if not checkMatkul:
            raise ValueError("Mata Kuliah tidak tersedia!")

        ta = db.query(TahunAjaran).filter_by(name=tahun_ajaran).first()
        if not ta:
            raise ValueError("Tahun Ajaran tidak tersedia!")

        pkActive = db.query(Perkuliahan).filter_by(id=id).first()
        if (
            (pkActive.mata_kuliah_id != checkMatkul.id)
            or (pkActive.tahun_ajaran_id != ta.id)
            or (pkActive.semester != semester)
            or (pkActive.kelas != kelas)
        ):
            raise ValueError("Data Perkuliahan tidak selaras!")

        checkPk = (
            db.query(Perkuliahan)
            .filter_by(mata_kuliah_id=checkMatkul.id)
            .filter_by(tahun_ajaran_id=ta.id)
            .filter_by(semester=semester)
            .filter_by(kelas=kelas)
            .first()
        )

        setattr(checkPk, "doc_status_id", int(DocStatus.MENUNGGU_UPLOAD_CPMK.value))
        db.commit()

        if not checkPk:
            raise ValueError("Perkuliahan tidak tersedia!")

        idx = 0
        headerLen = 2
        for value in data["data"]:
            if idx >= 7:
                dis = headerLen - len(value)
                if dis > 0:
                    for _ in range(0, dis):
                        value.append("")

                nim = str(value[0])
                full_name = str(value[1])

                char = ["(", "<", "%", ">", ")"]
                for ch in char:
                    full_name = full_name.replace(ch, "")

                if nim and full_name:
                    mhs = db.query(Mahasiswa).filter_by(nim=nim).first()
                    if not mhs:
                        mhs = Mahasiswa(
                            **{
                                "nim": nim,
                                "full_name": full_name.rsplit(" ", 1)[0]
                                .lower()
                                .title()
                                .strip(),
                                "prodi_id": 8,
                                "status_mhs_id": 1,
                            }
                        )
                        db.add(mhs)
                        db.commit()
                        db.refresh(mhs)

                    mapping = MappingMahasiswa(
                        **{"perkuliahan_id": checkPk.id, "mahasiswa_id": mhs.id}
                    )
                    db.add(mapping)
                    db.commit()

            idx += 1

        return {
            "code": status.HTTP_200_OK,
            "message": "Success Upload DPNA",
        }

    except Exception as e:
        print(e)
        db.rollback()
        err = str(e.args[0]).split("\n")
        data = {"message": err[errArray(len(err))]}
        raise HandlerCustom(data=data)


@app.get("/get-template/{id}", response_model=PerkuliahanResponseSchema)
async def bg_task_template(
    db: Session = Depends(db),
    background_tasks=BackgroundTasks,
    token: str = Header(default=None),
    id: int = None,
    # data: dict = None,
):
    # id = int(data["id"])
    checkExpDPNA = db.query(CheckExportDPNA).filter_by(perkuliahan_id=id).first()
    if not checkExpDPNA:
        background_tasks.add_task(get_template(db, id=id))
    else:
        dir = checkExpDPNA.template_name
        return FileResponse(path=dir, filename=dir.replace("files/", ""))


def get_template(db, id: int):
    pk = db.query(Perkuliahan).filter_by(id=id).first()
    matkul = mataKuliah.getByID(db, pk.mata_kuliah_id, "token")
    ta = tahunAjaran.getByID(db, pk.tahun_ajaran_id, "token")
    mapping = db.query(MappingMahasiswa).filter_by(perkuliahan_id=pk.id).all()

    wb = load_workbook("files/template_cpmk.xlsx")

    SH_CPMK = wb["CPMK-CPL"]
    SH_TUGAS = wb["NILAI TUGAS"]
    SH_PRAKTEK = wb["NILAI PRAKTEK"]
    SH_UTS = wb["NILAI UTS"]
    SH_UAS = wb["NILAI UAS"]
    SH_SIAP = wb["FORM NILAI SIAP"]

    SH_CPMK["C1"] = matkul.kode_mk
    SH_CPMK["C2"] = ta.tahun_ajaran
    SH_CPMK["C3"] = pk.semester
    SH_CPMK["C4"] = pk.kelas

    no = 1
    row = 8
    print(mapping)
    for map in mapping:
        mhs = db.query(Mahasiswa).filter_by(id=map.mahasiswa_id).first()
        SH_TUGAS["A" + str(row)] = no
        SH_TUGAS["B" + str(row)] = mhs.nim
        SH_TUGAS["C" + str(row)] = mhs.full_name

        SH_PRAKTEK["A" + str(row)] = no
        SH_PRAKTEK["B" + str(row)] = mhs.nim
        SH_PRAKTEK["C" + str(row)] = mhs.full_name

        SH_UTS["A" + str(row)] = no
        SH_UTS["B" + str(row)] = mhs.nim
        SH_UTS["C" + str(row)] = mhs.full_name

        SH_UAS["A" + str(row)] = no
        SH_UAS["B" + str(row)] = mhs.nim
        SH_UAS["C" + str(row)] = mhs.full_name

        SH_SIAP["A" + str(row)] = mhs.nim
        SH_SIAP["B" + str(row)] = mhs.full_name

        no += 1
        row += 1

    now = datetime.now().strftime("%Y_%m_%d-%I_%M_%S")
    path = "files/{}_{}_{}.xlsx".format(
        (matkul.mata_kuliah).lower().replace(" ", "_"), pk.semester.lower(), now
    )
    wb.save(path)

    exp = CheckExportDPNA(
        **{
            "perkuliahan_id": id,
            "template_name": path,
        }
    )
    db.add(exp)
    db.commit()


@app.post("/cpmk" + "-upload")
async def upload_cpmk(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    data: dict = None,
):
    id = data["id"]
    data = data["data"]

    try:
        SH_CPMK = data[0]
        SH_TUGAS = data[1]
        SH_PRAKTEK = data[2]
        SH_UTS = data[3]
        SH_UAS = data[4]

        # CPMK
        c1 = SH_CPMK[0][2]
        if len(c1.split("-")) != 2:
            raise ValueError("Format cell C1 (Kode MK - Matkul) tidak valid!")

        kode_mk = str(c1.split("-")[0]).replace(":", "").strip()
        tahun_ajaran = SH_CPMK[1][2]
        semester = SH_CPMK[2][2]
        kelas = str(SH_CPMK[3][2]).replace(":", "").strip()
        sks = str(SH_CPMK[8][2]).replace(":", "").strip()

        # Check If Related
        checkMatkul = db.query(MataKuliah).filter_by(kode_mk=kode_mk).first()
        if not checkMatkul:
            raise ValueError("Mata Kuliah tidak tersedia!")

        ta = db.query(TahunAjaran).filter_by(tahun_ajaran=tahun_ajaran).first()
        if not ta:
            raise ValueError("Tahun Ajaran tidak tersedia!")

        pkActive = db.query(Perkuliahan).filter_by(id=id).first()
        if (
            (pkActive.mata_kuliah_id != checkMatkul.id)
            or (pkActive.tahun_ajaran_id != ta.id)
            or (pkActive.semester != semester)
            or (pkActive.kelas != kelas)
        ):
            raise ValueError("Data Perkuliahan tidak selaras!")

        checkPk = (
            db.query(Perkuliahan)
            .filter_by(mata_kuliah_id=checkMatkul.id)
            .filter_by(tahun_ajaran_id=ta.id)
            .filter_by(semester=semester)
            .filter_by(kelas=kelas)
            .first()
        )

        if not checkPk:
            raise ValueError("Perkuliahan tidak tersedia!")

        perkuliahan.insert_cpl(db, checkPk.id, SH_CPMK)
        perkuliahan.insert_cpmk(db, checkPk.id, SH_CPMK)
        perkuliahan.insert_nilai(db, checkPk.id, SH_TUGAS, NilaiTugas, "tugas")
        perkuliahan.insert_nilai(db, checkPk.id, SH_PRAKTEK, NilaiPraktek, "praktek")
        perkuliahan.insert_nilai(db, checkPk.id, SH_UTS, NilaiUTS, "uts")
        perkuliahan.insert_nilai(db, checkPk.id, SH_UAS, NilaiUAS, "uas")

        return {
            "code": status.HTTP_200_OK,
            "message": "Success Upload CPMK",
        }

    except Exception as e:
        print(e)
        db.rollback()
        err = str(e.args[0]).split("\n")
        data = {"message": err[errArray(len(err))]}
        raise HandlerCustom(data=data)
