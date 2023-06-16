from fastapi import Request
from fastapi import Depends, status, Header

from controller import perkuliahan
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.schemas.perkuliahanSchema import (
    PerkuliahanResponseSchema,
    PerkuliahanCreateSchema,
    PerkuliahanUpdateSchema,
    PerkuliahanDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token
from db.models import (
    MataKuliah,
    User,
    UserRole,
    Perkuliahan,
    TahunAjaran,
    Mahasiswa,
    MappingMahasiswa,
)

PERKULIAHAN = "/perkuliahan"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(PERKULIAHAN + "s", response_model=PerkuliahanResponseSchema)
# @check_access_module
async def get_all_perkuliahan(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
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
# @check_access_module
async def get_perkuliahan(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = perkuliahan.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get perkuliahan",
        "data": data,
    }


@app.post(PERKULIAHAN, response_model=PerkuliahanResponseSchema)
# @check_access_module
async def submit_perkuliahan(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: PerkuliahanCreateSchema = None,
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
# @check_access_module
async def update_perkuliahan(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: PerkuliahanUpdateSchema = None,
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
# @check_access_module
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
        thn_ajaran = (data[0][1]).replace(":", "").strip()
        semester = (data[1][1]).replace(":", "").strip()

        if semester == "" or thn_ajaran == "":
            raise ValueError(
                "Tidak terdapat semester atau tahun ajaran pada row " + +str(idx)
            )

        headerLen = 10
        idx = 0
        for value in data:
            if idx >= 4 and len(value) > 0:
                dis = headerLen - len(value)
                if dis > 0:
                    for _ in range(0, dis):
                        value.append("")

                matkul = (value[0]).strip()
                kode = (value[1]).strip()
                kelas = (value[2]).strip()
                sks = ((value[3].strip().lower())).replace("sks", "")
                dosen1 = (value[4]).strip()
                nip_dosen1 = (value[5]).strip()
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
                    ta = TahunAjaran(**{"tahun_ajaran": thn_ajaran, "is_active": True})
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
        raise HandlerCustom(data=data)


@app.post("/dpna" + "-upload")
async def upload(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
    request: Request = None,
):
    header = data["data"]
    try:
        c1 = header[0][1]
        if len(c1.split("-")) != 2:
            raise ValueError("Format cell B1 (Kode MK - Matkul) tidak valid!")

        kode_mk = (c1.split("-")[0]).replace(":", "").strip()
        tahun_ajaran = (header[1][1]).replace(":", "").strip()
        semester = (header[2][1]).replace(":", "").strip()
        kelas = (header[3][1]).replace(":", "").strip()

        checkMatkul = db.query(MataKuliah).filter_by(kode_mk=kode_mk).first()
        if not checkMatkul:
            raise ValueError("Mata Kuliah tidak tersedia!")

        ta = db.query(TahunAjaran).filter_by(tahun_ajaran=tahun_ajaran).first()
        if not ta:
            raise ValueError("Tahun Ajaran tidak tersedia!")

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

        idx = 0
        headerLen = 2
        for value in data["data"]:
            if idx >= 16:
                dis = headerLen - len(value)
                if dis > 0:
                    for _ in range(0, dis):
                        value.append("")

                nim = str(value[0])
                full_name = str(value[1])

                if nim and full_name:
                    mhs = db.query(Mahasiswa).filter_by(nim=nim).first()
                    if not mhs:
                        mhs = Mahasiswa(
                            **{
                                "nim": nim,
                                "full_name": full_name,
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

    except Exception as e:
        print(e)
        db.rollback()
        err = str(e.args[0]).split("\n")
        data = {"message": err[errArray(len(err))]}
        raise HandlerCustom(data=data)
