from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz
from decimal import Decimal

from db.schemas.mappingMahasiswaSchema import MappingMahasiswaSchema
from db.schemas.cpmkSchema import CPMKSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseNilaiUasSchema(BaseModel):
    id: Optional[int] = None
    mapping_mhs_id: Optional[int] = None
    cpmk_id: Optional[int] = None

    nilai_cpmk: Optional[Decimal] = None
    bobot_cpmk: Optional[Decimal] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class NilaiUasSchema(BaseNilaiUasSchema):
    mappingMhs: Optional[MappingMahasiswaSchema] = None
    cpmk: Optional[CPMKSchema] = None

    class Config:
        orm_mode = True


class NilaiUasCreateSchema(BaseNilaiUasSchema):
    pass


class NilaiUasUpdateSchema(BaseNilaiUasSchema):
    id: int


class NilaiUasDeleteSchema(BaseModel):
    id: int


class NilaiUasResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[NilaiUasSchema], NilaiUasSchema] = None
    total: Optional[int] = None
