from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.prodiSchema import ProdiSchema
from db.schemas.perkuliahan2Schema import PerkuliahanSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseUserSchema(BaseModel):
    id: Optional[int] = None
    prodi_id: Optional[int] = None

    email: Optional[str] = None
    nip: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    email_verified_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class UserSchema(BaseUserSchema):
    prodi: Optional[ProdiSchema] = None
    perkuliahan: Optional[List[PerkuliahanSchema]] = None
    mahasiswa = []

    class Config:
        orm_mode = True


class UserCreateSchema(BaseUserSchema):
    pass


class UserUpdateSchema(BaseUserSchema):
    id: int


class UserDeleteSchema(BaseModel):
    id: int


class UserResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[UserSchema], UserSchema] = None
    total: Optional[int] = None
