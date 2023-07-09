from fastapi import Request
from fastapi import Depends, status, Header

from controller import assessmentMatkul
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.models import *
from db.database import Session
from db.schemas.assessmentMatkulSchema import (
    AssessmentMatkulResponseSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token
from sqlalchemy import cast, String, Date, desc, or_


ASSESSMENT_MATKUL = "/assessment-matkul"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


def helperRetrieveAssessmentMatkul(db, data, isEdit = False):
    for dt in data:
        listOfCPL = []

        setattr(dt, 'mataKuliah', dt.mataKuliah)
        setattr(dt, 'tahunAjaran', dt.tahunAjaran)
        setattr(dt, 'prodi', dt.prodi)
        setattr(dt, 'docstatus', dt.docstatus)

        mapMhs = db.query(MappingMahasiswa).\
            filter(MappingMahasiswa.perkuliahan_id == dt.id).\
            all()
        
        cplVal = []
        for map in mapMhs:
            cplMhs = db.query(CplMahasiswa).\
                filter(CplMahasiswa.mapping_mhs_id == map.id).\
                all()
            
            for cpl in cplMhs:
                cplVal.append(float(cpl.value))

        sumCplVal = float(sum(cplVal))
        sumCplDivision = len(cplVal)
        if sumCplDivision == 0:
            sumCplDivision = 1

        rerataCpl = "{:.2f}".format(float(sumCplVal / sumCplDivision)) 
        setattr(dt, 'rerataCpl', rerataCpl)

        cpmk = db.query(CPMK).filter_by(perkuliahan_id=dt.id).all()
        matkulInfo = []

        for cp in cpmk:
            sumSingleCpmk = []
            for map in mapMhs:
                cpmkVal = db.query(CpmkMahasiswa).\
                    filter(CpmkMahasiswa.mapping_mhs_id == map.id).\
                    filter(CpmkMahasiswa.cpmk_id == cp.id).\
                    all()
            
                for cpmk in cpmkVal:
                    sumSingleCpmk.append(float(cpmk.value))

            sumCpmkVal = float(sum(sumSingleCpmk))
            sumCpmkDivision = len(sumSingleCpmk)
            if sumCpmkDivision == 0:
                sumCpmkDivision = 1

            dictCPMK = {
                'id': cp.id,
                'name': cp.name,
                'statement': cp.statement,
                'value': "{:.2f}".format(float(sumCpmkVal / sumCpmkDivision)),
                'cpl': []
            }

            mapping = db.query(MappingCpmkCpl).filter_by(cpmk_id=cp.id).all()
            ids = []
            for map in mapping:
                cpl = db.query(CPL).filter_by(id=map.cpl_id).first()
                listOfCPL.append({'id': cpl.id, 'name': cpl.name})

                cplVal = []
                for mapM in mapMhs:
                    cplSingleVal = db.query(CplMahasiswa).\
                        filter(CplMahasiswa.mapping_mhs_id == mapM.id).\
                        filter(CplMahasiswa.cpl_id == map.cpl_id).\
                        all()
                
                    for single in cplSingleVal:
                        cplVal.append(float(single.value))
                
                sumSingleCplVal = float(sum(cplVal))
                sumSingleCplDivision = float(len(cplVal))
                if sumSingleCplDivision == 0:
                    sumSingleCplDivision = 1.0


                rerataSingleCpl = "{:.2f}".format(sumSingleCplVal / sumSingleCplDivision) 

                setattr(cpl, 'value', str(int(map.value) * 100) + '%')
                setattr(cpl, 'rerataOneCpl', rerataSingleCpl)

                if not cpl.id in ids:
                    ids.append(cpl.id)
                    dictCPMK['cpl'].append(cpl)

            matkulInfo.append(dictCPMK)

            #CPL in Header
            if isEdit:
                headerCPL = []
                for cpl in listOfCPL:
                    tempData = []
                    for map in mapMhs:
                        cplMhs = db.query(CplMahasiswa).\
                            filter(CplMahasiswa.mapping_mhs_id == map.id).\
                            filter(CplMahasiswa.cpl_id == cpl['id']).\
                            all()

                        for cplMh in cplMhs:
                            tempData.append(float(cplMh.value))

                    sumAllCPl = float(sum(tempData))
                    division = len(tempData)
                    if division == 0:
                        division = 1

                    headerCPL.append({'name': cpl['name'], 'value': sumAllCPl/division})

        if isEdit:
            setattr(dt, 'cpl', headerCPL)
            
        setattr(dt, 'cpmk', matkulInfo)


@app.get(ASSESSMENT_MATKUL + "s", response_model=AssessmentMatkulResponseSchema)
# @check_access_module
async def get_all_assessment_matkul(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = assessmentMatkul.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered assessment matkul",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = assessmentMatkul.getAllPaging(db, page, token)
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
    request: Request = None,
):
    data = (
        db.query(Perkuliahan)
        .filter_by(doc_status_id=3)
    )

    data_params = dict(request.query_params)
    if bool(data_params):
        for key in data_params:
            data = data.filter(cast(getattr(Perkuliahan, key), String).\
                            ilike("%{}%".format(data_params[key])))
       
    data = data.all()
    helperRetrieveAssessmentMatkul(db, data)

    return {
        "code": status.HTTP_200_OK,
        "message": "Success get assessment matkul",
        "data": data,
    }


@app.get(ASSESSMENT_MATKUL + "/{id}", response_model=AssessmentMatkulResponseSchema)
# @check_access_module
async def get_assessment_matkul(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = assessmentMatkul.getByID(db, id, token)

    pks = []
    legends = []
    for pk in data.children:
        row = db.query(Perkuliahan).filter_by(id=pk.perkuliahan_id).first()
        pks.append(row)
        legends.append(pk.perkuliahan.tahunAjaran.tahun_ajaran.replace('/', '-') + ' / ' + str(pk.perkuliahan.semester))

    helperRetrieveAssessmentMatkul(db, pks, True)
    setattr(data, 'legends', legends)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get assessment matkul",
        "data": data,
    }


@app.post(ASSESSMENT_MATKUL, response_model=AssessmentMatkulResponseSchema)
# @check_access_module
async def submit_assessment_matkul(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
):
    username = getUsername(token)
    res = assessmentMatkul.create(db, username, data)
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


@app.put(ASSESSMENT_MATKUL, response_model=AssessmentMatkulResponseSchema)
# @check_access_module
async def update_assessment_matkul(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
):
    username = getUsername(token)
    res = assessmentMatkul.update(db, username, data)
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
