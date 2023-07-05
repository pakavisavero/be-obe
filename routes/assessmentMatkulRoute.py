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

ASSESSMENT_MATKUL = "/assessment-matkul"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(ASSESSMENT_MATKUL + "s", response_model=SiklusProdiResponseSchema)
# @check_access_module
async def get_all_assessment_matkul(
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
            "message": "Success retrieve filtered assessment matkul",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = siklusProdi.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all assessment matkul",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(ASSESSMENT_MATKUL + "/option")
async def get_siklus_assessment_matkul(
    db: Session = Depends(db),
    token: str = Header(default=None),
):
    data = (
        db.query(Perkuliahan)
        .filter_by(doc_status_id=3)
        .all()
    )
    
    for dt in data:
        setattr(dt, 'mataKuliah', dt.mataKuliah)
        setattr(dt, 'tahunAjaran', dt.tahunAjaran)
        setattr(dt, 'prodi', dt.prodi)
        setattr(dt, 'docstatus', dt.docstatus)

        cpmk = db.query(CPMK).filter_by(perkuliahan_id=dt.id).all()
        matkulInfo = []

        for cp in cpmk:
            dictCPMK = {
                'name': cp.name,
                'statement': cp.statement,
                'cpl': []
            }

            mapping = db.query(MappingCpmkCpl).filter_by(cpmk_id=cp.id).all()
            for map in mapping:
                cpl = db.query(CPL).filter_by(id=map.cpl_id).first()
                dictCPMK['cpl'].append(cpl)

            matkulInfo.append(dictCPMK)

        setattr(dt, 'cpmk', matkulInfo)


    return {
        "code": status.HTTP_200_OK,
        "message": "Success get assessment matkul",
        "data": data,
    }


@app.get(ASSESSMENT_MATKUL + "/{id}", response_model=SiklusProdiResponseSchema)
# @check_access_module
async def get_assessment_matkul(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = siklusProdi.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get assessment matkul",
        "data": data,
    }


@app.post(ASSESSMENT_MATKUL, response_model=SiklusProdiResponseSchema)
# @check_access_module
async def submit_assessment_matkul(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
):
    username = getUsername(token)

    res = siklusProdi.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit assessment matkul",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit assessment matkul",
        }


@app.put(ASSESSMENT_MATKUL, response_model=SiklusProdiResponseSchema)
# @check_access_module
async def update_assessment_matkul(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
):
    username = getUsername(token)
    res = siklusProdi.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update assessment matkul",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update assessment matkul",
        }


@app.delete(ASSESSMENT_MATKUL)
# @check_access_module
async def delete_assessment_matkul(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete assessment matkul",
    }
