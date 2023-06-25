from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    BigInteger,
    Text,
    DECIMAL,
    LargeBinary,
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from datetime import datetime
import pytz

Base = declarative_base()

tz = pytz.timezone("Asia/Jakarta")


class ModuleGroup(Base):
    __tablename__ = "module_groups"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    module_name = Column(String(length=255))
    path = Column(String(length=255), nullable=True)
    icon = Column(String(length=255), nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)


class Module(Base):
    __tablename__ = "modules"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    module_group_id = Column(BigInteger, ForeignKey(ModuleGroup.id))

    module_name = Column(String(length=255))
    path = Column(String(length=255), nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    moduleGroup = relationship("ModuleGroup", foreign_keys=[module_group_id])


class Fakultas(Base):
    __tablename__ = "fakultas"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    nama_fakultas = Column(String(length=255))
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)


class Prodi(Base):
    __tablename__ = "prodis"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    fakultas_id = Column(BigInteger, ForeignKey(Fakultas.id))

    prodi = Column(String(length=255))
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    fakultas = relationship("Fakultas", foreign_keys=[fakultas_id])


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    prodi_id = Column(BigInteger, ForeignKey(Prodi.id))

    email = Column(String(length=255), unique=True)
    nip = Column(String(length=100), unique=True)
    username = Column(String(length=255), nullable=True)
    password = Column(LargeBinary)
    full_name = Column(String(length=255))
    email_verified_at = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    prodi = relationship("Prodi", foreign_keys=[prodi_id])


class RoleMaster(Base):
    __tablename__ = "role_masters"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    role_name = Column(String(length=255))
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey(User.id))
    role_id = Column(BigInteger, ForeignKey(RoleMaster.id))

    role_name = Column(String(length=255))
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    user = relationship("User", foreign_keys=[user_id])
    roleMaster = relationship("RoleMaster", foreign_keys=[role_id])


class StatusMahasiswa(Base):
    __tablename__ = "status_mahasiswas"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    status = Column(String(length=255))
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)


class Mahasiswa(Base):
    __tablename__ = "mahasiswas"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    prodi_id = Column(BigInteger, ForeignKey(Prodi.id))
    status_mhs_id = Column(BigInteger, ForeignKey(StatusMahasiswa.id))

    full_name = Column(String(length=255))
    nim = Column(String(length=100))
    semester = Column(Integer)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    prodi = relationship("Prodi", foreign_keys=[prodi_id])
    status = relationship("StatusMahasiswa", foreign_keys=[status_mhs_id])


class MahasiswaDoswal(Base):
    __tablename__ = "mahasiswa_doswals"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    mahasiswa_id = Column(BigInteger, ForeignKey(Mahasiswa.id))
    dosen_id = Column(BigInteger, ForeignKey(User.id))

    angkatan = Column(String(length=150))
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    mahasiswa = relationship("Mahasiswa", foreign_keys=[mahasiswa_id])
    dosen = relationship("User", foreign_keys=[dosen_id])


class Kurikulum(Base):
    __tablename__ = "kurikulums"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    name = Column(String(length=100))
    deskripsi = Column(String(length=200))
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)


class MataKuliah(Base):
    __tablename__ = "mata_kuliahs"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    kurikulum_id = Column(BigInteger, ForeignKey(Kurikulum.id))
    prodi_id = Column(BigInteger, ForeignKey(Prodi.id))

    kode_mk = Column(String(length=100))
    mata_kuliah = Column(String(length=200))
    sks = Column(String(length=200))
    is_konsen = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    kurikulum = relationship("Kurikulum", foreign_keys=[kurikulum_id])
    prodi = relationship("Prodi", foreign_keys=[prodi_id])


class TahunAjaran(Base):
    __tablename__ = "tahun_ajarans"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    name = Column(String(150))
    tahun_ajaran = Column(String(150))
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)


class DocStatusPK(Base):
    __tablename__ = "doc_status_pk"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    status = Column(String)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)


class Perkuliahan(Base):
    __tablename__ = "perkuliahans"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    dosen_id = Column(BigInteger, ForeignKey(User.id))
    dosen2_id = Column(BigInteger, ForeignKey(User.id), nullable=True)
    dosen3_id = Column(BigInteger, ForeignKey(User.id), nullable=True)
    pj_dosen_id = Column(BigInteger, ForeignKey(User.id))
    mata_kuliah_id = Column(BigInteger, ForeignKey(MataKuliah.id))
    prodi_id = Column(BigInteger, ForeignKey(Prodi.id))
    tahun_ajaran_id = Column(BigInteger, ForeignKey(TahunAjaran.id))
    doc_status_id = Column(BigInteger, ForeignKey(DocStatusPK.id))

    kelas = Column(String(length=100))
    semester = Column(String(length=200))
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    dosen1 = relationship("User", foreign_keys=[dosen_id])
    dosen2 = relationship("User", foreign_keys=[dosen2_id])
    dosen3 = relationship("User", foreign_keys=[dosen3_id])
    pjDosen = relationship("User", foreign_keys=[pj_dosen_id])
    mataKuliah = relationship("MataKuliah", foreign_keys=[mata_kuliah_id])
    prodi = relationship("Prodi", foreign_keys=[prodi_id])
    tahunAjaran = relationship("TahunAjaran", foreign_keys=[tahun_ajaran_id])
    docstatus = relationship("DocStatusPK", foreign_keys=[doc_status_id])


class Konsentrasi(Base):
    __tablename__ = "konsentrasis"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    konsentrasi = Column(String(length=100))
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)


class MatkulKonsentrasi(Base):
    __tablename__ = "matkul_konsentrasis"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    matkul_id = Column(BigInteger, ForeignKey(MataKuliah.id))
    konsentrasi_id = Column(BigInteger, ForeignKey(Konsentrasi.id))

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    matkul = relationship("MataKuliah", foreign_keys=[matkul_id])
    konsentrasi = relationship("Konsentrasi", foreign_keys=[konsentrasi_id])


class MahasiswaKonsentrasi(Base):
    __tablename__ = "mhs_konsentrasis"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    mahasiswa_id = Column(BigInteger, ForeignKey(Mahasiswa.id))
    konsentrasi_id = Column(BigInteger, ForeignKey(Konsentrasi.id))

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    mahasiswa = relationship("Mahasiswa", foreign_keys=[mahasiswa_id])
    konsentrasi = relationship("Konsentrasi", foreign_keys=[konsentrasi_id])


class MappingMahasiswa(Base):
    __tablename__ = "mapping_mahasiswas"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    perkuliahan_id = Column(BigInteger, ForeignKey(Perkuliahan.id))
    mahasiswa_id = Column(BigInteger, ForeignKey(Mahasiswa.id))
    status = Column(String)
    is_valid = Column(Boolean, default=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    perkuliahan = relationship("Perkuliahan", foreign_keys=[perkuliahan_id])
    mahasiswa = relationship("Mahasiswa", foreign_keys=[mahasiswa_id])


class KonsentrasiProdi(Base):
    __tablename__ = "konsentrasi_prodis"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    konsentrasi_id = Column(BigInteger, ForeignKey(Konsentrasi.id))
    prodi_id = Column(BigInteger, ForeignKey(Prodi.id))

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    konsentrasi = relationship("Konsentrasi", foreign_keys=[konsentrasi_id])
    prodi = relationship("Prodi", foreign_keys=[prodi_id])


class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    role_id = Column(BigInteger, ForeignKey(RoleMaster.id))
    module_id = Column(BigInteger, ForeignKey(Module.id))

    view = Column(Boolean, default=False)
    add = Column(Boolean, default=False)
    edit = Column(Boolean, default=False)
    printt = Column(Boolean, default=False)
    export = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    role = relationship("RoleMaster", foreign_keys=[role_id])
    module = relationship("Module", foreign_keys=[module_id])


class ChildModule(Base):
    __tablename__ = "child_modules"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    module_id = Column(BigInteger, ForeignKey(Module.id))

    module_name = Column(String(length=200))
    route = Column(String(length=150))
    is_active = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    module = relationship("Module", foreign_keys=[module_id])


class CPL(Base):
    __tablename__ = "cpls"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    prodi_id = Column(BigInteger, ForeignKey(Prodi.id))

    name = Column(String(length=200))
    statement = Column(Text())
    is_active = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    prodi = relationship("Prodi", foreign_keys=[prodi_id])


class CPMK(Base):
    __tablename__ = "cpmks"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    perkuliahan_id = Column(BigInteger, ForeignKey(Perkuliahan.id))

    name = Column(String(length=200))
    statement = Column(Text())
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    perkuliahan = relationship("Perkuliahan", foreign_keys=[perkuliahan_id])


class CpmkMahasiswa(Base):
    __tablename__ = "cpmk_mahasiswas"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    mapping_mhs_id = Column(BigInteger, ForeignKey(MappingMahasiswa.id))
    cpmk_id = Column(BigInteger, ForeignKey(CPMK.id))

    value = Column(String(length=200))

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    mappingMhs = relationship("MappingMahasiswa", foreign_keys=[mapping_mhs_id])
    cpmk = relationship("CPMK", foreign_keys=[cpmk_id])


class CplMahasiswa(Base):
    __tablename__ = "cpl_mahasiswas"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    mapping_mhs_id = Column(BigInteger, ForeignKey(MappingMahasiswa.id))
    cpl_id = Column(BigInteger, ForeignKey(CPL.id))

    value = Column(String(length=200))

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    mappingMhs = relationship("MappingMahasiswa", foreign_keys=[mapping_mhs_id])
    cpl = relationship("CPL", foreign_keys=[cpl_id])


class NilaiPokok(Base):
    __tablename__ = "nilai_pokoks"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    mapping_mhs_id = Column(BigInteger, ForeignKey(MappingMahasiswa.id))

    nilai_tugas = Column(DECIMAL)
    nilai_uts = Column(DECIMAL)
    nilai_uas = Column(DECIMAL)
    nilai_praktek = Column(DECIMAL)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    mappingMhs = relationship("MappingMahasiswa", foreign_keys=[mapping_mhs_id])


class NilaiTugas(Base):
    __tablename__ = "nilai_tugas"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    mapping_mhs_id = Column(BigInteger, ForeignKey(MappingMahasiswa.id))
    cpmk_id = Column(BigInteger, ForeignKey(CPMK.id))

    nilai_cpmk = Column(DECIMAL)
    bobot_cpmk = Column(DECIMAL)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    mappingMhs = relationship("MappingMahasiswa", foreign_keys=[mapping_mhs_id])
    cpmk = relationship("CPMK", foreign_keys=[cpmk_id])


class NilaiUAS(Base):
    __tablename__ = "nilai_uas"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    mapping_mhs_id = Column(BigInteger, ForeignKey(MappingMahasiswa.id))
    cpmk_id = Column(BigInteger, ForeignKey(CPMK.id))

    nilai_cpmk = Column(DECIMAL)
    bobot_cpmk = Column(DECIMAL)
    is_active = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    mappingMhs = relationship("MappingMahasiswa", foreign_keys=[mapping_mhs_id])
    cpmk = relationship("CPMK", foreign_keys=[cpmk_id])


class NilaiUTS(Base):
    __tablename__ = "nilai_uts"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    mapping_mhs_id = Column(BigInteger, ForeignKey(MappingMahasiswa.id))
    cpmk_id = Column(BigInteger, ForeignKey(CPMK.id))

    nilai_cpmk = Column(DECIMAL)
    bobot_cpmk = Column(DECIMAL)
    is_active = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    mappingMhs = relationship("MappingMahasiswa", foreign_keys=[mapping_mhs_id])
    cpmk = relationship("CPMK", foreign_keys=[cpmk_id])


class NilaiPraktek(Base):
    __tablename__ = "nilai_prakteks"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    mapping_mhs_id = Column(BigInteger, ForeignKey(MappingMahasiswa.id))
    cpmk_id = Column(BigInteger, ForeignKey(CPMK.id))

    nilai_cpmk = Column(DECIMAL)
    bobot_cpmk = Column(DECIMAL)
    is_active = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    mappingMhs = relationship("MappingMahasiswa", foreign_keys=[mapping_mhs_id])
    cpmk = relationship("CPMK", foreign_keys=[cpmk_id])


class MappingCpmkCpl(Base):
    __tablename__ = "mapping_cpmk_cpls"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    cpmk_id = Column(BigInteger, ForeignKey(CPMK.id))
    cpl_id = Column(BigInteger, ForeignKey(CPL.id))

    value = Column(String(150))
    is_active = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    cpmk = relationship("CPMK", foreign_keys=[cpmk_id])
    cpl = relationship("CPL", foreign_keys=[cpl_id])


class ProdiStruktural(Base):
    __tablename__ = "prodi_strukturals"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    prodi_id = Column(BigInteger, ForeignKey(Prodi.id))
    gpm_id = Column(BigInteger, ForeignKey(User.id))
    kaprodi_id = Column(BigInteger, ForeignKey(User.id))

    is_active = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    prodi = relationship("Prodi", foreign_keys=[prodi_id])
    gpm = relationship("User", foreign_keys=[gpm_id])
    kaprodi = relationship("User", foreign_keys=[kaprodi_id])


class PresentasePK(Base):
    __tablename__ = "persentase_pks"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    perkuliahan_id = Column(BigInteger, ForeignKey(Perkuliahan.id))

    nilai_tugas = Column(String(200))
    nilai_uts = Column(String(200))
    nilai_uas = Column(String(200))
    nilai_praktek = Column(String(200))
    is_active = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    perkuliahan = relationship("Perkuliahan", foreign_keys=[perkuliahan_id])


class CheckExportDPNA(Base):
    __tablename__ = "check_export_dpnas"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    perkuliahan_id = Column(BigInteger, ForeignKey(Perkuliahan.id))
    template_name = Column(Text())

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    perkuliahan = relationship("Perkuliahan", foreign_keys=[perkuliahan_id])


class EvaluasiMain(Base):
    __tablename__ = "evaluasi_mains"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    perkuliahan_id = Column(BigInteger, ForeignKey(Perkuliahan.id))

    rerata = Column(String())
    ambang = Column(String())

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    perkuliahan = relationship("Perkuliahan", foreign_keys=[perkuliahan_id])


class Evaluasi(Base):
    __tablename__ = "evaluasis"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    perkuliahan_id = Column(BigInteger, ForeignKey(Perkuliahan.id))
    cpmk_id = Column(BigInteger, ForeignKey(CPMK.id))

    rerata = Column(String())
    ambang = Column(String())
    memenuhi = Column(Boolean)

    analsis = Column(Text())
    rencana = Column(Text())

    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(String(length=120), nullable=True)
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    modified_by = Column(String(length=120), nullable=True)

    cpmk = relationship("CPMK", foreign_keys=[cpmk_id])
    perkuliahan = relationship("Perkuliahan", foreign_keys=[perkuliahan_id])
