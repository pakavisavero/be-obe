from fastapi import Request
from fastapi import Depends, status, Header

from controller import assessmentProdi
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.models import *
from db.database import Session
from db.schemas.assessmentProdiSchema import (
    AssessmentProdiResponseSchema,
)

ASSESSMENT_PRODI = "/assessment-prodi"

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
        query = assessmentProdi.getAllPagingFiltered(db, page, filtered_data, token)

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
