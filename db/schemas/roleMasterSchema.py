from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.prodiSchema import ProdiSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseRoleMasterSchema(BaseModel):
    id: Optional[int] = None

    role_name: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class RoleMasterSchema(BaseRoleMasterSchema):
    class Config:
        orm_mode = True


class RoleMasterCreateSchema(BaseRoleMasterSchema):
    pass


class RoleMasterUpdateSchema(BaseRoleMasterSchema):
    id: int


class RoleMasterDeleteSchema(BaseModel):
    id: int


class RoleMasterResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[RoleMasterSchema], RoleMasterSchema] = None
    total: Optional[int] = None
