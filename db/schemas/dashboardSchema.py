from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

tz = pytz.timezone("Asia/Jakarta")


class BaseDashboardSchema(BaseModel):
    jml_mahasiswa: Optional[int] = None
    jml_matkul: Optional[int] = None
    jml_prodi: Optional[int] = None


class DasboardSchema(BaseDashboardSchema):
    class Config:
        orm_mode = True


class DasboardCreateSchema(BaseDashboardSchema):
    pass


class DasboardUpdateSchema(BaseDashboardSchema):
    id: int


class DasboardDeleteSchema(BaseModel):
    id: int


class DasboardResponseSchema(BaseModel):
    code: int
    message: str
    data: DasboardSchema = None
    total: Optional[int] = None
