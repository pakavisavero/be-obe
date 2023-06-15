from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.prodiSchema import ProdiSchema
from db.schemas.kurikulumSchema import KurikulumSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseMataKuliahSchema(BaseModel):
    id: Optional[int] = None
    kurikulum_id: Optional[int] = None
    prodi_id: Optional[int] = None

    kode_mk: Optional[str] = None
    mata_kuliah: Optional[str] = None
    sks: Optional[str] = None
    is_konsen: Optional[bool] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class MataKuliahSchema(BaseMataKuliahSchema):
    kurikulum: Optional[ProdiSchema] = None
    prodi: Optional[KurikulumSchema] = None

    class Config:
        orm_mode = True


class MataKuliahCreateSchema(BaseMataKuliahSchema):
    pass


class MataKuliahUpdateSchema(BaseMataKuliahSchema):
    id: int


class MataKuliahDeleteSchema(BaseModel):
    id: int


class MataKuliahResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[MataKuliahSchema], MataKuliahSchema] = None
    total: Optional[int] = None
