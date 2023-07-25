from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.mataKuliahSchema import MataKuliahSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseLinkMataKuliahSchema(BaseModel):
    id: Optional[int] = None
    mata_kuliah_id: Optional[int] = None
    mapping_id: Optional[int] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class LinkMataKuliahSchema(BaseLinkMataKuliahSchema):
    mataKuliah: Optional[MataKuliahSchema] = None
    mapping: Optional[MataKuliahSchema] = None

    class Config:
        orm_mode = True


class LinkMataKuliahCreateSchema(BaseLinkMataKuliahSchema):
    pass


class LinkMataKuliahUpdateSchema(BaseLinkMataKuliahSchema):
    id: int


class LinkMataKuliahDeleteSchema(BaseModel):
    id: int


class LinkMataKuliahResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[LinkMataKuliahSchema], LinkMataKuliahSchema] = None
    total: Optional[int] = None
