from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.prodiSchema import ProdiSchema
from db.schemas.kurikulumSchema import KurikulumSchema

tz = pytz.timezone("Asia/Jakarta")


class BasePerkuliahanSchema(BaseModel):
    id: Optional[int] = None
    dosen_id: Optional[int] = None
    dosen2_id: Optional[int] = None
    dosen3_id: Optional[int] = None
    pj_dosen_id: Optional[int] = None
    mata_kuliah_id: Optional[int] = None
    prodi_id: Optional[int] = None

    kelas: Optional[str] = None
    tahun_ajaran: Optional[str] = None
    semester: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class PerkuliahanSchema(BasePerkuliahanSchema):
    dosen1: Optional[ProdiSchema] = None
    dosen2: Optional[KurikulumSchema] = None
    dosen3: Optional[KurikulumSchema] = None
    pjDosen: Optional[KurikulumSchema] = None
    mataKuliah: Optional[KurikulumSchema] = None
    prodi: Optional[KurikulumSchema] = None

    class Config:
        orm_mode = True


class PerkuliahanCreateSchema(BasePerkuliahanSchema):
    pass


class PerkuliahanUpdateSchema(BasePerkuliahanSchema):
    id: int


class PerkuliahanDeleteSchema(BaseModel):
    id: int


class PerkuliahanResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[PerkuliahanSchema], PerkuliahanSchema] = None
    total: Optional[int] = None
