from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.userSchema import UserSchema
from db.schemas.roleMasterSchema import RoleMasterSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseUserRoleSchema(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    role_id: Optional[int] = None

    role_name: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class UserRoleSchema(BaseUserRoleSchema):
    user: Optional[UserSchema] = None
    roleMaster: Optional[RoleMasterSchema] = None

    class Config:
        orm_mode = True


class UserRoleCreateSchema(BaseUserRoleSchema):
    pass


class UserRoleUpdateSchema(BaseUserRoleSchema):
    id: int


class UserRoleDeleteSchema(BaseModel):
    id: int


class UserRoleResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[UserRoleSchema], UserRoleSchema] = None
    total: Optional[int] = None
