from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.moduleGroupSchema import ModuleGroupSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseFakultasSchema(BaseModel):
    id: Optional[int] = None

    nama_fakultas: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class FakultasSchema(BaseFakultasSchema):
    class Config:
        orm_mode = True


class FakultasCreateSchema(BaseFakultasSchema):
    pass


class FakultasUpdateSchema(BaseFakultasSchema):
    id: int


class FakultasDeleteSchema(BaseModel):
    id: int


class FakultasResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[FakultasSchema], FakultasSchema] = None
    total: Optional[int] = None
