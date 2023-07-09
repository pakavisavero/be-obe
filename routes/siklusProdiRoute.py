from fastapi import Request
from fastapi import Depends, status, Header

from controller import siklusProdi
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.models import *
from db.database import Session
from db.schemas.siklusProdiSchema import (
    SiklusProdiResponseSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token


SIKLUS_PRODI = "/siklus-prodi"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(SIKLUS_PRODI + "s", response_model=SiklusProdiResponseSchema)
# @check_access_module
async def get_all_siklus_prodi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = siklusProdi.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered siklus prodi",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = siklusProdi.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all siklus prodi",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(SIKLUS_PRODI + "/option")
async def get_siklus_prodi_option(
    db: Session = Depends(db),
    token: str = Header(default=None),
):
    data = []
    semester = ["Gasal", "Genap"]
    tahunAjaran = db.query(TahunAjaran).all()

    id = 1
    for ta in tahunAjaran:
        for sem in semester:
            temp = {"id": id, "tahunAjaran": ta, "semester": sem, "cpl": []}

            pk = (
                db.query(Perkuliahan)
                .filter_by(tahun_ajaran_id=ta.id)
                .filter_by(semester=sem)
                .filter_by(doc_status_id=3)
                .all()
            )

            ids = []
            for p in pk:
                cpmk = db.query(CPMK).filter_by(perkuliahan_id=p.id).all()
                for cp in cpmk:
                    mapping = db.query(MappingCpmkCpl).filter_by(cpmk_id=cp.id).all()
                    for map in mapping:
                        cpl = db.query(CPL).filter_by(id=map.cpl_id).first()
                        if not cpl.id in ids:
                            ids.append(cpl.id)
                            temp["cpl"].append(cpl)

                # setattr(p, 'copyId', p.id)
            data.append(temp)
            id += 1

    return {
        "code": status.HTTP_200_OK,
        "message": "Success get siklus prodi",
        "data": data,
    }


@app.get(SIKLUS_PRODI + "/{id}", response_model=SiklusProdiResponseSchema)
# @check_access_module
async def get_siklus_prodi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = siklusProdi.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get siklus prodi",
        "data": data,
    }


@app.post(SIKLUS_PRODI, response_model=SiklusProdiResponseSchema)
# @check_access_module
async def submit_siklus_prodi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
):
    username = getUsername(token)

    res = siklusProdi.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit siklus prodi",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit siklus prodi",
        }


@app.put(SIKLUS_PRODI, response_model=SiklusProdiResponseSchema)
# @check_access_module
async def update_siklus_prodi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
):
    username = getUsername(token)
    res = siklusProdi.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update siklus prodi",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update siklus prodi",
        }


@app.delete(SIKLUS_PRODI)
# @check_access_module
async def delete_siklus_prodi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete siklus prodi",
    }
