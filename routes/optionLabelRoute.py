from fastapi import Request
from fastapi import Depends, status, Header

from routes.route import app
from controller.utils import help_filter, check_access_module

from db.session import db, getUsername
from db.database import Session
from db.models import *
from db.helper import decode_token

from db.schemas.fakultasSchema import FakultasResponseSchema
from db.schemas.kurikulumSchema import KurikulumResponseSchema
from db.schemas.mataKuliahSchema import MataKuliahResponseSchema
from db.schemas.prodiSchema import ProdiResponseSchema
from db.schemas.statusMahasiswaSchema import StatusMahasiswaResponseSchema
from db.schemas.tahunAjaranSchema import TahunAjaranResponseSchema
from db.schemas.userSchema import UserResponseSchema
from db.schemas.docstatuspkSchema import DocStatusPKResponseSchema

from controller import (
    fakultas,
    kurikulum,
    mataKuliah,
    prodi,
    statusMahasiswa,
    tahunAjaran,
    user,
    docStatusPk,
)


@app.get("/option/user", response_model=UserResponseSchema)
async def get_option_user(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = user.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered user",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = user.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all user",
            "data": query["data"],
            "total": query["total"],
        }


@app.get("/option/fakultas", response_model=FakultasResponseSchema)
async def get_option_fakultas(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = fakultas.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered fakultas",
            "data": query["data"],
            "total": query["total"],
        }

    else:
        query = fakultas.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all fakultas",
            "data": query["data"],
            "total": query["total"],
        }


@app.get("/option/kurikulum", response_model=KurikulumResponseSchema)
async def get_option_kurikulum(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = kurikulum.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered kurikulum",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = kurikulum.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all kurikulum",
            "data": query["data"],
            "total": query["total"],
        }


@app.get("/option/mata-kuliah", response_model=MataKuliahResponseSchema)
async def get_option_mata_kuliah(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = mataKuliah.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered mata kuliah",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = mataKuliah.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all mata kuliah",
            "data": query["data"],
            "total": query["total"],
        }


@app.get("/option/prodi", response_model=ProdiResponseSchema)
async def get_option_prodi(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = prodi.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered prodi",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = prodi.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all prodi",
            "data": query["data"],
            "total": query["total"],
        }


@app.get("/option/status-mahasiswa", response_model=StatusMahasiswaResponseSchema)
async def get_option_status_mahasiswa(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = statusMahasiswa.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered status mahasiswa",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = statusMahasiswa.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all status mahasiswa",
            "data": query["data"],
            "total": query["total"],
        }


@app.get("/option/tahun-ajaran", response_model=TahunAjaranResponseSchema)
async def get_option_tahun_ajaran(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = tahunAjaran.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered tahun ajaran",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = tahunAjaran.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all tahun ajaran",
            "data": query["data"],
            "total": query["total"],
        }


@app.get("/option/doc-status-pk", response_model=DocStatusPKResponseSchema)
async def get_option_doc_status_pk(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    filtered_data = help_filter(request)
    if filtered_data:
        query = docStatusPk.getAllPagingFiltered(db, page, filtered_data, token)

        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve filtered doc status perkuliahan",
            "data": query["data"],
            "total": query["total"],
        }
    else:
        query = docStatusPk.getAllPaging(db, page, token)
        return {
            "code": status.HTTP_200_OK,
            "message": "Success retrieve all doc status perkuliahan",
            "data": query["data"],
            "total": query["total"],
        }
