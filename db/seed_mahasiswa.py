import pandas as pd
import json
from database import Session
from models import Mahasiswa, User, MahasiswaDoswal

xls = pd.ExcelFile("files/mahasiswa/data_mahasiswa_2016_to_2022.xlsx")
df = pd.read_excel(xls)
result = df
result.fillna("", inplace=True)

db = Session()

mahasiswa = []

for i, row in list(result.iterrows()):
    tempMhs = {
        "full_name": row[1],
        "nim": row[0],
        "prodi_id": 8,
        "status_mhs_id": 1,
        "nip": row[3],
    }

    mahasiswa.append(tempMhs)


for mhs in mahasiswa:
    nip = mhs["nip"]

    del mhs["nip"]
    dt = Mahasiswa(**mhs)
    db.add(dt)
    db.commit()
    db.refresh(dt)

    dosen_id = db.query(User).filter_by(nip=str(nip)).first()
    dw = MahasiswaDoswal(
        **{
            "mahasiswa_id": dt.id,
            "dosen_id": dosen_id.id,
            "angkatan": "20" + str(mhs["nim"])[6:8],
        }
    )
    db.add(dw)
    db.commit()

    # print("success add mahasiswa " + mhs["full_name"])
