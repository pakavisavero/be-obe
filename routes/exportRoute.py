from fastapi import Request
from fastapi import Depends, status, Header
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks

from controller import *
from controller.utils import export_file
from routes.route import app
from controller.utils import to_dict

from db.models import *
from db.session import db, getUsername
from db.database import Session

import os


def remove_file(path: str) -> None:
    os.unlink(path)


@app.get("/api/export/mahasiswa")
async def export_mahasiswa(
    db: Session = Depends(db),
    token: str = Header(default=None),
    background_tasks: BackgroundTasks = None,
):
    element = db.query(Mahasiswa).all()
    columns = ["Program Studi", "Status", "Nama Lengkap", "NIM", "Semester"]
    modified = [
        {
            'name': 'prodi_id',
            'relation': 'prodi',
            'opt': 'prodi'
        },
        {
            'name': 'status_mhs_id',
            'relation': 'status',
            'opt': 'status'
        }
    ]

    data_list = [to_dict(is_parent=True, row=item, modified=modified)
                 for item in element]
    file_response = export_file(columns, data_list, 'mahasiswa')

    background_tasks.add_task(remove_file, file_response)
    return FileResponse(
        path=file_response,
        filename=file_response.replace("export_files/", "")
    )


@app.get("/api/export/dosen")
async def export_dosen(
    db: Session = Depends(db),
    token: str = Header(default=None),
    background_tasks: BackgroundTasks = None,
):
    query = db.query(UserRole).filter_by(role_id=3).all()
    element = [q.user for q in query]

    columns = ["Program Studi", "Email", "NIP", "Nama Lengkap"]
    modified = [
        {
            'name': 'prodi_id',
            'relation': 'prodi',
            'opt': 'prodi'
        },
    ]

    data_list = [to_dict(is_parent=True, row=item, modified=modified, xtraIgnore=['password', 'email_verified_at', 'last_login', 'username'])
                 for item in element]
    file_response = export_file(columns, data_list, 'dosen')

    background_tasks.add_task(remove_file, file_response)
    return FileResponse(
        path=file_response,
        filename=file_response.replace("export_files/", "")
    )


@app.get("/api/export/mata-kuliah")
async def export_mata_kuliah(
    db: Session = Depends(db),
    token: str = Header(default=None),
    background_tasks: BackgroundTasks = None,
):
    element = db.query(MataKuliah).all()
    columns = ["Kurikulum", "Program Studi", "Kode MK", "Mata Kuliah"]
    modified = [
        {
            'name': 'kurikulum_id',
            'relation': 'kurikulum',
            'opt': 'name'
        },
        {
            'name': 'prodi_id',
            'relation': 'prodi',
            'opt': 'prodi'
        }
    ]

    data_list = [to_dict(is_parent=True, row=item, modified=modified, xtraIgnore=['is_konsen', 'sks'])
                 for item in element]
    file_response = export_file(columns, data_list, 'mata_kuliah')

    background_tasks.add_task(remove_file, file_response)
    return FileResponse(
        path=file_response,
        filename=file_response.replace("export_files/", "")
    )


@app.get("/api/export/kbm-aktif")
async def export_kbm_aktif(
    db: Session = Depends(db),
    token: str = Header(default=None),
    background_tasks: BackgroundTasks = None,
):
    element = db.query(Perkuliahan).filter_by(is_active=True).all()
    columns = ["Dosen I", "Dosen II", "Dosen III", "PJ Dosen",
               "Mata Kuliah", "Program Studi", "Tahun Ajaran", "Kelas", "Semester"]
    modified = [
        {
            'name': 'dosen_id',
            'relation': 'dosen1',
            'opt': 'full_name'
        },
        {
            'name': 'dosen2_id',
            'relation': 'dosen2',
            'opt': 'full_name'
        },
        {
            'name': 'dosen3_id',
            'relation': 'dosen3',
            'opt': 'full_name'
        },
        {
            'name': 'pj_dosen_id',
            'relation': 'pjDosen',
            'opt': 'full_name'
        },
        {
            'name': 'mata_kuliah_id',
            'relation': 'mataKuliah',
            'opt': 'mata_kuliah'
        },
        {
            'name': 'prodi_id',
            'relation': 'prodi',
            'opt': 'prodi'
        },
        {
            'name': 'tahun_ajaran_id',
            'relation': 'tahunAjaran',
            'opt': 'tahun_ajaran'
        }
    ]

    data_list = [to_dict(is_parent=True, row=item, modified=modified, xtraIgnore=['doc_status_id', 'sks'])
                 for item in element]
    file_response = export_file(columns, data_list, 'kbm_aktif')

    background_tasks.add_task(remove_file, file_response)
    return FileResponse(
        path=file_response,
        filename=file_response.replace("export_files/", "")
    )


@app.get("/api/export/history-kbm")
async def export_history_kbm(
    db: Session = Depends(db),
    token: str = Header(default=None),
    background_tasks: BackgroundTasks = None,
):
    element = db.query(Perkuliahan).filter_by(is_active=False).all()
    columns = ["Dosen I", "Dosen II", "Dosen III", "PJ Dosen",
               "Mata Kuliah", "Program Studi", "Tahun Ajaran", "Kelas", "Semester"]
    modified = [
        {
            'name': 'dosen_id',
            'relation': 'dosen1',
            'opt': 'full_name'
        },
        {
            'name': 'dosen2_id',
            'relation': 'dosen2',
            'opt': 'full_name'
        },
        {
            'name': 'dosen3_id',
            'relation': 'dosen3',
            'opt': 'full_name'
        },
        {
            'name': 'pj_dosen_id',
            'relation': 'pjDosen',
            'opt': 'full_name'
        },
        {
            'name': 'mata_kuliah_id',
            'relation': 'mataKuliah',
            'opt': 'mata_kuliah'
        },
        {
            'name': 'prodi_id',
            'relation': 'prodi',
            'opt': 'prodi'
        },
        {
            'name': 'tahun_ajaran_id',
            'relation': 'tahunAjaran',
            'opt': 'tahun_ajaran'
        }
    ]

    data_list = [to_dict(is_parent=True, row=item, modified=modified, xtraIgnore=['doc_status_id', 'sks'])
                 for item in element]
    file_response = export_file(columns, data_list, 'history_kbm')

    background_tasks.add_task(remove_file, file_response)
    return FileResponse(
        path=file_response,
        filename=file_response.replace("export_files/", "")
    )
