from fastapi import Request
from fastapi import Depends, status, Header

from routes.route import app
from db.session import db, getUsername
from db.database import Session

from HandlerCustom import HandlerCustom
from db.helper import decode_token
from db.models import Mahasiswa, MataKuliah, Prodi

DASHBOARD = "/api/dashboard"


@app.get(DASHBOARD + "s")
# @check_access_module
async def get_dashboards(
    db: Session = Depends(db),
    token: str = Header(default=None),
    request: Request = None,
    page: int = 0,
):
    jml_mahasiswa = db.query(Mahasiswa).count()
    jml_matkul = db.query(MataKuliah).count()
    jml_prodi = db.query(Prodi).count()

    data = {
        "jml_mahasiswa": jml_mahasiswa,
        "jml_matkul": jml_matkul,
        "jml_prodi": jml_prodi,
    }

    print(data)

    return {
        "code": status.HTTP_200_OK,
        "message": "success retrieve data!",
        "data": data,
    }
