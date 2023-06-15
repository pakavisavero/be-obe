from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

tz = pytz.timezone("Asia/Jakarta")


class BaseKurikulumSchema(BaseModel):
    id: Optional[int] = None

    name: Optional[str] = None
    deskripsi: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class KurikulumSchema(BaseKurikulumSchema):
    class Config:
        orm_mode = True


class KurikulumCreateSchema(BaseKurikulumSchema):
    pass


class KurikulumUpdateSchema(BaseKurikulumSchema):
    id: int


class KurikulumDeleteSchema(BaseModel):
    id: int


class KurikulumResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[KurikulumSchema], KurikulumSchema] = None
    total: Optional[int] = None
