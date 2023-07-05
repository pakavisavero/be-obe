from database import Session
from models import *

db = Session()

for x in range(882, 1063):
    db.query(CplMahasiswa).filter(CplMahasiswa.mapping_mhs_id==x).delete()
    db.query(CpmkMahasiswa).filter(CpmkMahasiswa.mapping_mhs_id==x).delete()
    db.query(NilaiPokok).filter(NilaiPokok.mapping_mhs_id==x).delete()
    db.commit()


db.query(PresentasePK).filter(PresentasePK.perkuliahan_id==447).delete()
db.query(Perkuliahan).filter(Perkuliahan.id==447).delete()

db.commit()

