from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.prodiSchema import ProdiSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseStatusMahasiswaSchema(BaseModel):
    id: Optional[int] = None

    status: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class StatusMahasiswaSchema(BaseStatusMahasiswaSchema):
    class Config:
        orm_mode = True


class StatusMahasiswaCreateSchema(BaseStatusMahasiswaSchema):
    pass


class StatusMahasiswaUpdateSchema(BaseStatusMahasiswaSchema):
    id: int


class StatusMahasiswaDeleteSchema(BaseModel):
    id: int


class StatusMahasiswaResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[StatusMahasiswaSchema], StatusMahasiswaSchema] = None
    total: Optional[int] = None
