from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz
from decimal import Decimal

from db.schemas.mappingMahasiswaSchema import MappingMahasiswaSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseNilaiPokokSchema(BaseModel):
    id: Optional[int] = None
    mapping_mhs_id: Optional[int] = None

    nilai_tugas: Optional[Decimal] = None
    nilai_praktek: Optional[Decimal] = None
    nilai_uts: Optional[Decimal] = None
    nilai_uas: Optional[Decimal] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class NilaiPokokSchema(BaseNilaiPokokSchema):
    mappingMhs: Optional[MappingMahasiswaSchema] = None

    class Config:
        orm_mode = True


class NilaiPokokCreateSchema(BaseNilaiPokokSchema):
    pass


class NilaiPokokUpdateSchema(BaseNilaiPokokSchema):
    id: int


class NilaiPokokDeleteSchema(BaseModel):
    id: int


class NilaiPokokResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[NilaiPokokSchema], NilaiPokokSchema] = None
    total: Optional[int] = None
