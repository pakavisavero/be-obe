from fastapi import Request
from fastapi import Depends, status, Header

from controller import cpl
from routes.route import app
from controller.utils import help_filter, check_access_module

from db.models import *
from db.models import CPL as CPLModel
from db.session import db, getUsername
from db.database import Session
from db.schemas.cplSchema import (
    CPLResponseSchema,
    CPLCreateSchema,
    CPLUpdateSchema,
    CPLDeleteSchema,
)

from HandlerCustom import HandlerCustom
from db.helper import decode_token

CPL = "/cpl"


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


@app.get(CPL + "s", response_model=CPLResponseSchema)
# @check_access_module
async def get_all_cpl(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = cpl.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered cpl",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = cpl.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all cpl",
            "data": query["data"],
            "total": query["total"],
        }


@app.get(CPL + "/{id}", response_model=CPLResponseSchema)
# @check_access_module
async def get_cpl(
    db: Session = Depends(db),
    token: str = Header(default=None),
    id: int = None,
):
    data = cpl.getByID(db, id, token)
    return {
        "code": status.HTTP_200_OK,
        "message": "Success get cpl",
        "data": data,
    }


@app.post(CPL, response_model=CPLResponseSchema)
# @check_access_module
async def submit_cpl(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: CPLCreateSchema = None,
):
    username = getUsername(token)

    res = cpl.create(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success submit cpl",
            "data": res,
        }

    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error submit cpl",
        }


@app.put(CPL, response_model=CPLResponseSchema)
# @check_access_module
async def update_cpl(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: CPLUpdateSchema = None,
):
    username = getUsername(token)
    res = cpl.update(db, username, data)
    if res:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success update cpl",
            "data": data,
        }
    else:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "error update cpl",
        }


@app.delete(CPL)
# @check_access_module
async def delete_cpl(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: CPLDeleteSchema = None,
):
    return {
        "code": status.HTTP_200_OK,
        "message": "Success delete cpl",
    }


@app.post("/get-perkuliahan-by-cpl")
# @check_access_module
async def get_cpl_by_perkuliahan(
    db: Session = Depends(db),
    token: str = Header(default=None),
    data: dict = None,
):
    cpl_id = int(data["cpl_id"])
    ta_id = int(data["tahun_ajaran_id"])
    semester = data["semester"]

    data = []
    mapping = db.query(MappingCpmkCpl).filter_by(cpl_id=cpl_id).all()

    ids = []
    for map in mapping:
        cpmk = db.query(CPMK).filter_by(id=map.cpmk_id).first()
        pk = db.query(Perkuliahan).filter_by(id=cpmk.perkuliahan_id).first()

        if (
            (pk.tahun_ajaran_id == ta_id)
            and (pk.semester == semester)
            and (pk.doc_status_id == 3)
        ):
            if not pk.id in ids:
                jmlMhs = 0
                total = 0.0
                mappingMhs = (
                    db.query(MappingMahasiswa).filter_by(perkuliahan_id=pk.id).all()
                )
                for mhs in mappingMhs:
                    cplValue = (
                        db.query(CplMahasiswa)
                        .filter_by(cpl_id=cpl_id)
                        .filter_by(mapping_mhs_id=mhs.id)
                        .first()
                    )
                    if cplValue:
                        val = cplValue.value
                        jmlMhs += 1
                        total += float(val)

                ids.append(pk.id)
                setattr(pk, "mataKuliah", pk.mataKuliah)
                setattr(pk, "dosen1", pk.dosen1)
                setattr(pk, "tahunAjaran", pk.tahunAjaran)
                setattr(pk, "total", "{:.2f}".format(total / jmlMhs))
                data.append(pk)

    return {
        "code": status.HTTP_200_OK,
        "message": "Success get cpl",
        "data": data,
    }
