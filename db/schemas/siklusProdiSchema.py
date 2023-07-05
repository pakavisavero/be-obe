from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.siklusProdiDetailSchema import SiklusProdiDetailSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseSiklusProdiSchema(BaseModel):
    id: Optional[int] = None

    name: Optional[str] = None
    description: Optional[str] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class SiklusProdiSchema(BaseSiklusProdiSchema):
    children: List[SiklusProdiDetailSchema] = None

    class Config:
        orm_mode = True


class SiklusProdiCreateSchema(BaseSiklusProdiSchema):
    pass


class SiklusProdiUpdateSchema(BaseSiklusProdiSchema):
    id: int


class SiklusProdiDeleteSchema(BaseModel):
    id: int


class SiklusProdiResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[SiklusProdiSchema], SiklusProdiSchema] = None
    total: Optional[int] = None
