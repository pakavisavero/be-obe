from database import Session
from models import *

db = Session()


pks = db.query(Perkuliahan).filter_by(id=1385).all()
for pk in pks:
    pk = pk.id
    db.query(CheckExportDPNA).filter_by(perkuliahan_id=pk).delete()
    db.query(SiklusProdiDetail).filter_by(perkuliahan_id=pk).delete()
    db.query(CheckExportPortofolio).filter_by(perkuliahan_id=pk).delete()
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
    db.query(Perkuliahan).filter_by(
        id=pk).update({'doc_status_id': 1})

    db.commit()
