from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.prodiSchema import ProdiSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseCPLSchema(BaseModel):
    id: Optional[int] = None
    prodi_id: Optional[int] = None

    name: Optional[str] = None
    statement: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class CPLSchema(BaseCPLSchema):
    prodi: Optional[ProdiSchema] = None

    class Config:
        orm_mode = True


class CPLCreateSchema(BaseCPLSchema):
    pass


class CPLUpdateSchema(BaseCPLSchema):
    id: int


class CPLDeleteSchema(BaseModel):
    id: int


class CPLResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[CPLSchema], CPLSchema] = None
    total: Optional[int] = None
