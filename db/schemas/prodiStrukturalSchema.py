from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.prodiSchema import ProdiSchema
from db.schemas.userSchema import UserSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseProdiStrukturalSchema(BaseModel):
    id: Optional[int] = None
    prodi_id: Optional[int] = None
    gpm_id: Optional[int] = None
    kaprodi_id: Optional[int] = None

    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class ProdiStrukturalSchema(BaseProdiStrukturalSchema):
    prodi: Optional[ProdiSchema] = None
    gpm: Optional[UserSchema] = None
    kaprodi: Optional[UserSchema] = None

    class Config:
        orm_mode = True


class ProdiStrukturalCreateSchema(BaseProdiStrukturalSchema):
    pass


class ProdiStrukturalUpdateSchema(BaseProdiStrukturalSchema):
    id: int


class ProdiStrukturalDeleteSchema(BaseModel):
    id: int


class ProdiStrukturalResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[ProdiStrukturalSchema], ProdiStrukturalSchema] = None
    total: Optional[int] = None
