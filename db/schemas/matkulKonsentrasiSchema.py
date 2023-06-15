from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.mataKuliahSchema import MataKuliahSchema
from db.schemas.konsentrasiSchema import KonsentrasiSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseMatkulKonsentrasiSchema(BaseModel):
    id: Optional[int] = None
    matkul_id: Optional[int] = None
    konsentrasi_id: Optional[int] = None

    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class MatkulKonsentrasiSchema(BaseMatkulKonsentrasiSchema):
    matkul: Optional[MataKuliahSchema] = None
    konsentrasi: Optional[KonsentrasiSchema] = None

    class Config:
        orm_mode = True


class MatkulKonsentrasiCreateSchema(BaseMatkulKonsentrasiSchema):
    pass


class MatkulKonsentrasiUpdateSchema(BaseMatkulKonsentrasiSchema):
    id: int


class MatkulKonsentrasiDeleteSchema(BaseModel):
    id: int


class MatkulKonsentrasiResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[MatkulKonsentrasiSchema], MatkulKonsentrasiSchema] = None
    total: Optional[int] = None
