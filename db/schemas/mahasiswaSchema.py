from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.prodiSchema import ProdiSchema
from db.schemas.statusMahasiswaSchema import StatusMahasiswaSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseMahasiswaSchema(BaseModel):
    id: Optional[int] = None
    prodi_id: Optional[int] = None
    status_mhs_id: Optional[int] = None

    full_name: Optional[str] = None
    nim: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class MahasiswaSchema(BaseMahasiswaSchema):
    prodi: Optional[ProdiSchema] = None
    status: Optional[StatusMahasiswaSchema] = None

    class Config:
        orm_mode = True


class MahasiswaCreateSchema(BaseMahasiswaSchema):
    pass


class MahasiswaUpdateSchema(BaseMahasiswaSchema):
    id: int


class MahasiswaDeleteSchema(BaseModel):
    id: int


class MahasiswaResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[MahasiswaSchema], MahasiswaSchema] = None
    total: Optional[int] = None
