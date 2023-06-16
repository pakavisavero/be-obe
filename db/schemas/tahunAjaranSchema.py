from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

tz = pytz.timezone("Asia/Jakarta")


class BaseTahunAjaranSchema(BaseModel):
    id: Optional[int] = None

    tahun_ajaran: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class TahunAjaranSchema(BaseTahunAjaranSchema):
    class Config:
        orm_mode = True


class TahunAjaranCreateSchema(BaseTahunAjaranSchema):
    pass


class TahunAjaranUpdateSchema(BaseTahunAjaranSchema):
    id: int


class TahunAjaranDeleteSchema(BaseModel):
    id: int


class TahunAjaranResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[TahunAjaranSchema], TahunAjaranSchema] = None
    total: Optional[int] = None
