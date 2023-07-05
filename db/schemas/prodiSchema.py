from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.fakultasSchema import FakultasSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseProdiSchema(BaseModel):
    id: Optional[int] = None
    fakultas_id: Optional[int] = None

    prodi: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class ProdiSchema(BaseProdiSchema):
    fakultas: Optional[FakultasSchema] = None

    class Config:
        orm_mode = True


class ProdiCreateSchema(BaseProdiSchema):
    pass


class ProdiUpdateSchema(BaseProdiSchema):
    id: int


class ProdiDeleteSchema(BaseModel):
    id: int


class ProdiResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[ProdiSchema], ProdiSchema] = None
    total: Optional[int] = None
