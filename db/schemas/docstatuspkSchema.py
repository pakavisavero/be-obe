from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

tz = pytz.timezone("Asia/Jakarta")


class DocStatusPKSchema(BaseModel):
    id: Optional[int] = None

    status: Optional[str] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class DocStatusPKSchema(DocStatusPKSchema):
    class Config:
        orm_mode = True


class DocStatusPKCreateSchema(DocStatusPKSchema):
    pass


class DocStatusPKUpdateSchema(DocStatusPKSchema):
    id: int


class DocStatusPKDeleteSchema(BaseModel):
    id: int


class DocStatusPKResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[DocStatusPKSchema], DocStatusPKSchema] = None
    total: Optional[int] = None
