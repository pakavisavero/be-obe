from fastapi import Request
from fastapi import Depends, status, Header
from fastapi.responses import FileResponse

from controller import *
from controller.utils import export_file
from routes.route import app
from controller.utils import to_dict

from db.models import *
from db.session import db, getUsername
from db.database import Session


@app.get("/api/export/mahasiswa")
async def export_mahasiswa(
    db: Session = Depends(db),
    token: str = Header(default=None),
):
    element = db.query(Mahasiswa).all()
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
    file_response = export_file(data_list, 'mahasiswa')
    return FileResponse(path=file_response)


@app.get("/api/export/dosen")
async def export_dosen(
    db: Session = Depends(db),
    token: str = Header(default=None),
):
    query = db.query(UserRole).filter_by(role_id=3).all()
    element = [q.user for q in query]

    modified = [
        {
            'name': 'prodi_id',
            'relation': 'prodi',
            'opt': 'prodi'
        },
    ]

    data_list = [to_dict(is_parent=True, row=item, modified=modified, xtraIgnore=['password', 'email_verified_at', 'last_login', 'username'])
                 for item in element]
    file_response = export_file(data_list, 'dosen')
    return FileResponse(path=file_response)


@app.get("/api/export/mata-kuliah")
async def export_mata_kuliah(
    db: Session = Depends(db),
    token: str = Header(default=None),
):
    element = db.query(MataKuliah).all()
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
    file_response = export_file(data_list, 'mata_kuliah')
    return FileResponse(path=file_response)
