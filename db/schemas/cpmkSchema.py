from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.perkuliahanSchema import PerkuliahanSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseCPMKSchema(BaseModel):
    id: Optional[int] = None
    perkuliahan_id: Optional[int] = None

    name: Optional[str] = None
    statement: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class CPMKSchema(BaseCPMKSchema):
    perkuliahan: Optional[PerkuliahanSchema] = None

    class Config:
        orm_mode = True


class CPMKCreateSchema(BaseCPMKSchema):
    pass


class CPMKUpdateSchema(BaseCPMKSchema):
    id: int


class CPMKDeleteSchema(BaseModel):
    id: int


class CPMKResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[CPMKSchema], CPMKSchema] = None
    total: Optional[int] = None
