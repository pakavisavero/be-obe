from fastapi import Request
from fastapi import Depends, status, Header

from controller import assessmentProdi
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername, getUserId
from db.models import *
from db.database import Session
from db.schemas.assessmentProdiSchema import (
    AssessmentProdiResponseSchema,
)

ASSESSMENT_PRODI = "/api/assessment-prodi"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(ASSESSMENT_PRODI + "s", response_model=AssessmentProdiResponseSchema)
# @check_access_module
async def get_all_assessment_prodi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = assessmentProdi.getAllPagingFiltered(
            db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered assessment prodi",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = assessmentProdi.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all assessment prodi",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(ASSESSMENT_PRODI + "/{id}", response_model=AssessmentProdiResponseSchema)
# @check_access_module
async def get_assessment_prodi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = assessmentProdi.getByID(db, id, token)

    return {
        "code": status.HTTP_200_OK,
        "message": "Success get assessment prodi",
        "data": data,
    }


@app.post(ASSESSMENT_PRODI, response_model=AssessmentProdiResponseSchema)
# @check_access_module
async def submit_assessment_prodi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
):
    username = getUsername(token)
    res = assessmentProdi.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit assessment prodi",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit assessment prodi",
        }


@app.put(ASSESSMENT_PRODI, response_model=AssessmentProdiResponseSchema)
# @check_access_module
async def update_assessment_prodi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
):
    username = getUsername(token)
    res = assessmentProdi.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update assessment prodi",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update assessment prodi",
        }


@app.delete(ASSESSMENT_PRODI)
# @check_access_module
async def delete_assessment_prodi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete assessment prodi",
    }


@app.get('/api/get-pdf-assessment-prodi/{id}')
# @check_access_module
async def get_pdf_assessment_prodi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    id: int = None
):
    user = db.query(User).filter_by(id=getUserId(token)).first()
    prodi_id = user.prodi_id

    data = []
    listSiklus = []

    cpls = db.query(CPL).filter_by(prodi_id=prodi_id).all()
    assessment = db.query(AssessmentProdi).filter_by(id=id).first()

    for cpl in cpls:
        # GET Assessment Prodi Detail
        dataSiklus = {
            'cpl': cpl.name.replace('CPL', 'PK ')
        }

        for asse in assessment.children:
            # GET Siklus
            siklus = asse.siklus
            values = 0
            sum = 0

            for detail in siklus.children:
                if cpl.id == detail.cpl_id:
                    pk = detail.perkuliahan_id
                    mapping = db.query(MappingMahasiswa).filter_by(
                        perkuliahan_id=pk).all()
                    for map in mapping:
                        cplMhs = db.query(CplMahasiswa).\
                            filter_by(mapping_mhs_id=map.id).\
                            filter_by(cpl_id=cpl.id).\
                            first()

                        values += float(cplMhs.value)
                        sum += 1

            # Prevent Zero Division
            if sum == 0:
                sum = 1

            if not siklus.name in listSiklus:
                listSiklus.append(siklus.name)

            dataSiklus[siklus.name] = round(values / sum / 25, 2)

        data.append(dataSiklus)

    return {
        "code": status.HTTP_200_OK,
        "message": "Success get assessment prodi data!",
        "data": {
            'pks': data,
            'siklus': listSiklus,
        },
    }
