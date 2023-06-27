from fastapi import Request
from fastapi import Depends, status, Header

from controller import assessment
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.models import *
from db.database import Session
from db.schemas.assessmentSchema import (
    AssessmentResponseSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

ASSESSMENT = "/assessment"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(ASSESSMENT + "s", response_model=AssessmentResponseSchema)
# @check_access_module
async def get_all_assessment(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = assessment.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered assessment",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = assessment.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all assessment",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(ASSESSMENT + "/option")
async def get_assessment_option(
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

            data.append(temp)
            id += 1

    return {
        "code": status.HTTP_200_OK,
        "message": "Success get assessment",
        "data": data,
    }


@app.get(ASSESSMENT + "/{id}", response_model=AssessmentResponseSchema)
# @check_access_module
async def get_assessment(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = assessment.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get assessment",
        "data": data,
    }


@app.post(ASSESSMENT, response_model=AssessmentResponseSchema)
# @check_access_module
async def submit_assessment(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
):
    username = getUsername(token)

    res = assessment.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit assessment",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit assessment",
        }


@app.put(ASSESSMENT, response_model=AssessmentResponseSchema)
# @check_access_module
async def update_assessment(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
):
    username = getUsername(token)
    res = assessment.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update assessment",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update assessment",
        }


@app.delete(ASSESSMENT)
# @check_access_module
async def delete_assessment(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete assessment",
    }
