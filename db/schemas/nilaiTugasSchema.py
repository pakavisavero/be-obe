from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz
from decimal import Decimal

from db.schemas.mappingMahasiswaSchema import MappingMahasiswaSchema
from db.schemas.cpmkSchema import CPMKSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseNilaiTugasSchema(BaseModel):
    id: Optional[int] = None
    mapping_mhs_id: Optional[int] = None
    cpmk_id: Optional[int] = None

    nilai_tugas: Optional[Decimal] = None
    nilai_cpmk: Optional[Decimal] = None
    bobot_cpmk: Optional[Decimal] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class NilaiTugasSchema(BaseNilaiTugasSchema):
    mappingMhs: Optional[MappingMahasiswaSchema] = None
    cpmk: Optional[CPMKSchema] = None

    class Config:
        orm_mode = True


class NilaiTugasCreateSchema(BaseNilaiTugasSchema):
    pass


class NilaiTugasUpdateSchema(BaseNilaiTugasSchema):
    id: int


class NilaiTugasDeleteSchema(BaseModel):
    id: int


class NilaiTugasResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[NilaiTugasSchema], NilaiTugasSchema] = None
    total: Optional[int] = None
