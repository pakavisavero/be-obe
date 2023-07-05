from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.mahasiswaSchema import MahasiswaSchema
from db.schemas.userSchema import UserSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseMahasiswaDoswalSchema(BaseModel):
    id: Optional[int] = None
    mahasiswa_id: Optional[int] = None
    dosen_id: Optional[int] = None

    angkatan: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class MahasiswaDoswalSchema(BaseMahasiswaDoswalSchema):
    mahasiswa: Optional[MahasiswaSchema] = None
    dosen: Optional[UserSchema] = None

    class Config:
        orm_mode = True


class MahasiswaDoswalCreateSchema(BaseMahasiswaDoswalSchema):
    pass


class MahasiswaDoswalUpdateSchema(BaseMahasiswaDoswalSchema):
    id: int


class MahasiswaDoswalDeleteSchema(BaseModel):
    id: int


class MahasiswaDoswalResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[MahasiswaDoswalSchema], MahasiswaDoswalSchema] = None
    total: Optional[int] = None
