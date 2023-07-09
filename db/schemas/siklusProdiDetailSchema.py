from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.tahunAjaranSchema import TahunAjaranSchema
from db.schemas.perkuliahanSchema import PerkuliahanSchema
from db.schemas.cplSchema import CPLSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseSiklusProdiDetailSchema(BaseModel):
    id: Optional[int] = None
    parent_id: int
    perkuliahan_id: int
    cpl_id: int

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class SiklusProdiDetailSchema(BaseSiklusProdiDetailSchema):
    tahunAjaran: Optional[TahunAjaranSchema] = None
    perkuliahan: Optional[PerkuliahanSchema] = None
    cpl: Optional[CPLSchema] = None

    class Config:
        orm_mode = True


class SiklusProdiDetailCreateSchema(BaseSiklusProdiDetailSchema):
    pass


class SiklusProdiDetailUpdateSchema(BaseSiklusProdiDetailSchema):
    id: int


class SiklusProdiDetailDeleteSchema(BaseModel):
    id: int


class SiklusProdiDetailResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[SiklusProdiDetailSchema], SiklusProdiDetailSchema] = None
    total: Optional[int] = None
