from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

tz = pytz.timezone("Asia/Jakarta")


class BaseKonsentrasiSchema(BaseModel):
    id: Optional[int] = None

    konsentrasi: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class KonsentrasiSchema(BaseKonsentrasiSchema):
    class Config:
        orm_mode = True


class KonsentrasiCreateSchema(BaseKonsentrasiSchema):
    pass


class KonsentrasiUpdateSchema(BaseKonsentrasiSchema):
    id: int


class KonsentrasiDeleteSchema(BaseModel):
    id: int


class KonsentrasiResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[KonsentrasiSchema], KonsentrasiSchema] = None
    total: Optional[int] = None
