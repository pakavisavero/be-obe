from fastapi import FastAPI
from fastapi import Depends
from db.session import db

app = FastAPI(dependencies=[Depends(db)])

from routes import (
    cplRoute,
    cpmkRoute,
    fakultasRoute,
    konsentrasiProdiRoute,
    konsentrasiRoute,
    kurikulumRoute,
    mahasiswaDoswalRoute,
    mahasiswaKonsentrasiRoute,
    mahasiswaRoute,
    mappingCpmkCplRoute,
    mataKuliahRoute,
    matkulKonsentrasiRoute,
    moduleGroupRoute,
    moduleRoute,
    nilaiPraktekRoute,
    nilaiTugasRoute,
    nilaiUasRoute,
    nilaiUtsRoute,
    perkuliahanRoute,
    presentasePkRoute,
    prodiRoute,
    prodiStrukturalRoute,
    roleMasterRoute,
    rolePermissionRoute,
    statusMahasiswaRoute,
    userRoleRoute,
    userRoute,
    dashboardRoute,
    tahunAjaranRoute,
    loginRoute,
    optionLabelRoute,
    assessmentRoute
)
