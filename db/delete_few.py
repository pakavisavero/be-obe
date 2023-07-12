from database import Session
from models import *

db = Session()


pks = db.query(Perkuliahan).all()
for pk in pks:
    pk = pk.id
    db.query(CheckExportDPNA).filter_by(perkuliahan_id=pk).delete()
    base_cpmk = db.query(CPMK).filter_by(perkuliahan_id=pk)

    cpmks = base_cpmk.all()
    for cpmk in cpmks:
        db.query(CpmkMahasiswa).filter_by(cpmk_id=cpmk.id).delete()
        db.query(Evaluasi).filter_by(cpmk_id=cpmk.id).delete()
        db.query(MappingCpmkCpl).filter_by(cpmk_id=cpmk.id).delete()
        db.query(NilaiUAS).filter_by(cpmk_id=cpmk.id).delete()
        db.query(NilaiTugas).filter_by(cpmk_id=cpmk.id).delete()
        db.query(NilaiUTS).filter_by(cpmk_id=cpmk.id).delete()
        db.query(NilaiPraktek).filter_by(cpmk_id=cpmk.id).delete()
        db.query(NilaiPraktek).filter_by(cpmk_id=cpmk.id).delete()

    base_cpmk.delete()
    db.query(EvaluasiMain).filter_by(perkuliahan_id=pk).delete()

    base_mapping_mhs = db.query(MappingMahasiswa).filter_by(perkuliahan_id=pk)
    mapping_mhs = base_mapping_mhs.all()

    for map in mapping_mhs:
        db.query(CplMahasiswa).filter_by(mapping_mhs_id=map.id).delete()
        db.query(NilaiPokok).filter_by(mapping_mhs_id=map.id).delete()

    base_mapping_mhs.delete()
    db.query(PresentasePK).filter_by(perkuliahan_id=pk).delete()
    db.query(Perkuliahan).filter_by(id=pk).delete()


# for x in range(882, 1063):
#     db.query(CplMahasiswa).filter(CplMahasiswa.mapping_mhs_id==x).delete()
#     db.query(CpmkMahasiswa).filter(CpmkMahasiswa.mapping_mhs_id==x).delete()
#     db.query(NilaiPokok).filter(NilaiPokok.mapping_mhs_id==x).delete()
#     db.commit()


# db.query(PresentasePK).filter(PresentasePK.perkuliahan_id==447).delete()
# db.query(Perkuliahan).filter(Perkuliahan.id==447).delete()

    db.commit()

# for i in range(3, 31, 3):
#     db.query(CpmkMahasiswa).filter(CpmkMahasiswa.cpmk_id == i).delete()
#     db.query(Evaluasi).filter(Evaluasi.cpmk_id == i).delete()
#     db.query(CPMK).filter(CPMK.id == i).delete()
#     db.commit()