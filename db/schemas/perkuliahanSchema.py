from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.userSchema import UserSchema
from db.schemas.prodiSchema import ProdiSchema
from db.schemas.mataKuliahSchema import MataKuliahSchema
from db.schemas.tahunAjaranSchema import TahunAjaranSchema

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
    semester: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class PerkuliahanSchema(BasePerkuliahanSchema):
    dosen1: Optional[UserSchema] = None
    dosen2: Optional[UserSchema] = None
    dosen3: Optional[UserSchema] = None
    pjDosen: Optional[UserSchema] = None
    mataKuliah: Optional[MataKuliahSchema] = None
    prodi: Optional[ProdiSchema] = None
    tahunAjaran: Optional[TahunAjaranSchema] = None

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
